"use client";
import { useEffect, useState } from 'react';

const SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA';

const DAILY_QUESTIONS = 3;
const PASS_THRESHOLD = 3; // 3/3 全對才升級
const MAX_LEVEL = 14;

const LEVEL_NAMES = [
  '', // index 0 unused
  '新手', '初學者', '見習生', '學徒', '實習生',
  '中級', '進階', '高級', '專家', '大師',
  '宗師', '王者', '傳奇', '神話',
];

type TopicId = 'lower_limb' | 'cervical';

interface Topic {
  id: TopicId;
  table: string;
  label: string;
  emoji: string;
  description: string;
}

const TOPICS: Topic[] = [
  { id: 'lower_limb', table: 'anatomy_questions_lower_limb', label: '下肢解剖', emoji: '🦵', description: '腳踝、膝蓋、髖關節、肌肉、神經' },
  { id: 'cervical',   table: 'anatomy_questions_cervical_advanced', label: '頸椎進階', emoji: '🦴', description: '寰椎、樞椎、頸椎結構與功能' },
];

interface Question {
  id: string | number;
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
  level: number;
  qimage_url: string;
  image_url: string;
}

interface TopicProgress {
  unlockedLevel: number;          // 1..14
  lastPlayedDate: string | null;  // 'YYYY-MM-DD' (Asia/Taipei)
  todayQuestionIds: (string | number)[];
  todayResults: (boolean | null)[];
  totalDaysPlayed: number;
}

interface Progress {
  topics: Record<TopicId, TopicProgress>;
}

const STORAGE_KEY = 'anatomy-quiz-progress-v1';

function emptyTopicProgress(): TopicProgress {
  return { unlockedLevel: 1, lastPlayedDate: null, todayQuestionIds: [], todayResults: [], totalDaysPlayed: 0 };
}

function loadProgress(): Progress {
  if (typeof window === 'undefined') return { topics: { lower_limb: emptyTopicProgress(), cervical: emptyTopicProgress() } };
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) throw new Error('no progress');
    const parsed = JSON.parse(raw);
    return {
      topics: {
        lower_limb: { ...emptyTopicProgress(), ...(parsed.topics?.lower_limb || {}) },
        cervical:   { ...emptyTopicProgress(), ...(parsed.topics?.cervical   || {}) },
      },
    };
  } catch {
    return { topics: { lower_limb: emptyTopicProgress(), cervical: emptyTopicProgress() } };
  }
}

function saveProgress(p: Progress) {
  if (typeof window !== 'undefined') localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
}

function todayInTaipei(): string {
  const fmt = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Taipei', year: 'numeric', month: '2-digit', day: '2-digit' });
  return fmt.format(new Date()); // 'YYYY-MM-DD'
}

function msUntilTaipeiMidnight(): number {
  const tpNow = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Taipei' }));
  const next = new Date(tpNow);
  next.setHours(24, 0, 0, 0);
  return next.getTime() - tpNow.getTime();
}

type View = 'topic_select' | 'daily_intro' | 'playing' | 'result' | 'locked';

export default function GamePlayPage() {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [topic, setTopic] = useState<Topic | null>(null);
  const [view, setView] = useState<View>('topic_select');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [allQuestions, setAllQuestions] = useState<Question[]>([]);
  const [todayQs, setTodayQs] = useState<Question[]>([]);
  const [qIndex, setQIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [flash, setFlash] = useState<'right' | 'wrong' | null>(null);
  const [didLevelUp, setDidLevelUp] = useState(false);
  const [showLevelUpAnim, setShowLevelUpAnim] = useState(false);

  useEffect(() => {
    setProgress(loadProgress());
  }, []);

  function tp(): TopicProgress | null {
    if (!progress || !topic) return null;
    return progress.topics[topic.id];
  }

  function startTopic(t: Topic) {
    if (!progress) return;
    setTopic(t);
    const tProg = progress.topics[t.id];
    const today = todayInTaipei();

    // 已過期：清空今日狀態
    if (tProg.lastPlayedDate !== today) {
      const fresh: TopicProgress = { ...tProg, lastPlayedDate: null, todayQuestionIds: [], todayResults: [] };
      const next = { ...progress, topics: { ...progress.topics, [t.id]: fresh } };
      setProgress(next); saveProgress(next);
      setView('daily_intro');
      loadQuestions(t);
      return;
    }

    // 今天已完成
    if (tProg.todayResults.length === DAILY_QUESTIONS) {
      setView('locked');
      return;
    }

    // 今天有未完成的題目，繼續
    if (tProg.todayQuestionIds.length > 0) {
      setView('playing');
      loadQuestions(t, tProg.todayQuestionIds);
      setQIndex(tProg.todayResults.length);
      return;
    }

    setView('daily_intro');
    loadQuestions(t);
  }

  async function loadQuestions(t: Topic, restoreIds?: (string | number)[]) {
    try {
      setLoading(true); setError(null);
      const { createClient } = await import('@supabase/supabase-js');
      const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
      const { data, error: fetchErr } = await supabase.from(t.table).select('*');
      if (fetchErr) throw new Error('載入題目失敗: ' + fetchErr.message);
      if (!data || data.length === 0) throw new Error('題庫為空');
      const qs: Question[] = data.map(item => ({
        id: item.id,
        question: item.question,
        options: [item.option_1, item.option_2, item.option_3, item.option_4].filter(o => o && String(o).trim()),
        correct_answer: (item.correct_option || 1) - 1,
        explanation: item.explanation || '',
        level: item.level || 1,
        qimage_url: item.qimage_url || '',
        image_url: item.image_url || '',
      }));
      setAllQuestions(qs);
      if (restoreIds) {
        const restored = restoreIds.map(id => qs.find(q => String(q.id) === String(id))).filter(Boolean) as Question[];
        setTodayQs(restored);
      }
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : '載入失敗');
      setLoading(false);
    }
  }

  function beginToday() {
    if (!progress || !topic) return;
    const tProg = progress.topics[topic.id];
    const lvQs = allQuestions.filter(q => q.level === tProg.unlockedLevel);
    const pool = lvQs.length > 0 ? lvQs : allQuestions;
    const shuffled = [...pool].sort(() => Math.random() - 0.5);
    const picked = shuffled.slice(0, Math.min(DAILY_QUESTIONS, shuffled.length));
    while (picked.length < DAILY_QUESTIONS && pool.length > 0) {
      picked.push(pool[Math.floor(Math.random() * pool.length)]);
    }
    setTodayQs(picked);
    setQIndex(0); setSelectedAnswer(null); setShowExplanation(false); setFlash(null); setDidLevelUp(false);

    const today = todayInTaipei();
    const updated: TopicProgress = {
      ...tProg,
      lastPlayedDate: today,
      todayQuestionIds: picked.map(q => q.id),
      todayResults: [],
      totalDaysPlayed: tProg.totalDaysPlayed + (tProg.lastPlayedDate === today ? 0 : 1),
    };
    const next = { ...progress, topics: { ...progress.topics, [topic.id]: updated } };
    setProgress(next); saveProgress(next);
    setView('playing');
  }

  function selectAnswer(idx: number) {
    if (showExplanation) return;
    setSelectedAnswer(idx);
  }

  function submitAnswer() {
    if (selectedAnswer === null || !topic || !progress) return;
    const q = todayQs[qIndex];
    const isCorrect = selectedAnswer === q.correct_answer;
    setFlash(isCorrect ? 'right' : 'wrong');
    setTimeout(() => setFlash(null), 800);
    setShowExplanation(true);

    const tProg = progress.topics[topic.id];
    const newResults = [...tProg.todayResults, isCorrect];
    const updated: TopicProgress = { ...tProg, todayResults: newResults };
    const next = { ...progress, topics: { ...progress.topics, [topic.id]: updated } };
    setProgress(next); saveProgress(next);
  }

  function nextOrFinish() {
    if (!progress || !topic) return;
    if (qIndex < DAILY_QUESTIONS - 1) {
      setQIndex(qIndex + 1); setSelectedAnswer(null); setShowExplanation(false);
      return;
    }
    // 結算
    const tProg = progress.topics[topic.id];
    const correct = tProg.todayResults.filter(Boolean).length;
    if (correct >= PASS_THRESHOLD && tProg.unlockedLevel < MAX_LEVEL) {
      const updated: TopicProgress = { ...tProg, unlockedLevel: tProg.unlockedLevel + 1 };
      const next = { ...progress, topics: { ...progress.topics, [topic.id]: updated } };
      setProgress(next); saveProgress(next);
      setDidLevelUp(true); setShowLevelUpAnim(true);
      setTimeout(() => setShowLevelUpAnim(false), 2400);
    }
    setView('result');
  }

  function backToTopicSelect() {
    setTopic(null); setView('topic_select');
    setAllQuestions([]); setTodayQs([]); setQIndex(0);
    setSelectedAnswer(null); setShowExplanation(false); setFlash(null); setDidLevelUp(false);
  }

  // ============ Render ============

  // Loading / error overlays
  if (loading && view !== 'topic_select') return <ScreenWrap><Spinner /></ScreenWrap>;
  if (error) return <ScreenWrap><ErrorBox msg={error} onBack={backToTopicSelect} /></ScreenWrap>;

  if (view === 'topic_select' || !topic) {
    return (
      <ScreenWrap>
        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <h1 style={{ fontSize: '2.2rem', marginBottom: 6, color: '#1C1C1C' }}>🧠 解剖咬一口</h1>
          <p style={{ color: '#666', margin: 0 }}>選擇你今天想練習的題庫</p>
        </div>
        <div style={{ display: 'grid', gap: 14, width: '100%', maxWidth: 480 }}>
          {TOPICS.map(t => {
            const lvl = progress?.topics[t.id].unlockedLevel ?? 1;
            const days = progress?.topics[t.id].totalDaysPlayed ?? 0;
            return (
              <button key={t.id} onClick={() => startTopic(t)} style={cardBtn()}>
                <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
                  <img src={`/level-assets/level_${lvl}.webp`} alt="" style={{ width: 64, height: 64, objectFit: 'contain' }} />
                  <div style={{ flex: 1, textAlign: 'left' }}>
                    <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#1C1C1C' }}>{t.emoji} {t.label}</div>
                    <div style={{ fontSize: '0.9rem', color: '#888', marginTop: 2 }}>{t.description}</div>
                    <div style={{ fontSize: '0.85rem', color: '#C57B57', marginTop: 6, fontWeight: 600 }}>
                      Lv {lvl}/{MAX_LEVEL} · {LEVEL_NAMES[lvl]}{days > 0 && ` · 已挑戰 ${days} 天`}
                    </div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </ScreenWrap>
    );
  }

  const tProg = tp()!;

  if (view === 'locked') {
    const correct = tProg.todayResults.filter(Boolean).length;
    return (
      <ScreenWrap>
        <Card>
          <h2 style={{ marginTop: 0, textAlign: 'center' }}>🌙 今日挑戰已完成</h2>
          <div style={{ textAlign: 'center', margin: '16px 0' }}>
            <img src={`/level-assets/level_${tProg.unlockedLevel}_poster.webp`} alt="" style={{ width: '100%', maxWidth: 280, borderRadius: 12 }} />
          </div>
          <p style={{ textAlign: 'center', color: '#666' }}>
            今天答對 <b>{correct}/{DAILY_QUESTIONS}</b>，目前 <b>Lv {tProg.unlockedLevel} {LEVEL_NAMES[tProg.unlockedLevel]}</b>
          </p>
          <ResetCountdown />
          <BackBtn onClick={backToTopicSelect} />
        </Card>
      </ScreenWrap>
    );
  }

  if (view === 'daily_intro') {
    return (
      <ScreenWrap>
        <Card>
          <div style={{ textAlign: 'center' }}>
            <img src={`/level-assets/level_${tProg.unlockedLevel}_poster.webp`} alt="" style={{ width: '100%', maxWidth: 320, borderRadius: 12, marginBottom: 16 }} />
            <h2 style={{ margin: '0 0 6px' }}>第 {tProg.totalDaysPlayed + 1} 天挑戰</h2>
            <div style={{ color: '#C57B57', fontWeight: 700, fontSize: '1.1rem' }}>
              Lv {tProg.unlockedLevel} · {LEVEL_NAMES[tProg.unlockedLevel]}
            </div>
            <p style={{ color: '#666', margin: '14px 0' }}>今天 3 題，全對才能升級</p>
            <button onClick={beginToday} style={primaryBtn()}>🎯 開始挑戰</button>
            <BackBtn onClick={backToTopicSelect} />
          </div>
        </Card>
      </ScreenWrap>
    );
  }

  if (view === 'result') {
    const correct = tProg.todayResults.filter(Boolean).length;
    const passed = correct >= PASS_THRESHOLD;
    const newLevel = tProg.unlockedLevel; // 已經 ++ 了
    const shownLevel = didLevelUp ? newLevel : newLevel;
    return (
      <ScreenWrap>
        {showLevelUpAnim && (
          <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, animation: 'fadein 0.3s' }}>
            <img src="/level-assets/levelup.webp" alt="升級" style={{ width: '80%', maxWidth: 400, animation: 'pop 0.5s' }} />
          </div>
        )}
        <Card>
          <div style={{ textAlign: 'center' }}>
            <h2 style={{ margin: '0 0 8px' }}>{passed ? '🎉 通關！' : '加油！'}</h2>
            <p style={{ color: '#666', marginTop: 0 }}>今日答對 <b style={{ color: passed ? '#4caf50' : '#B85C38', fontSize: '1.4rem' }}>{correct}/{DAILY_QUESTIONS}</b></p>
            {didLevelUp && (
              <div style={{ background: 'linear-gradient(135deg, #fff3cd, #ffe69c)', padding: 16, borderRadius: 12, margin: '12px 0' }}>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 8 }}>🆙 升級！</div>
                <div style={{ color: '#8B4513', fontWeight: 600 }}>Lv {shownLevel} · {LEVEL_NAMES[shownLevel]}</div>
              </div>
            )}
            <img src={`/level-assets/level_${shownLevel}_poster.webp`} alt="" style={{ width: '100%', maxWidth: 280, borderRadius: 12, margin: '8px 0' }} />
            {!passed && <p style={{ color: '#666', fontSize: '0.9rem' }}>沒關係，明天可以再挑戰一次！</p>}
            <ResetCountdown />
            <BackBtn onClick={backToTopicSelect} />
          </div>
        </Card>
        <style jsx global>{`
          @keyframes fadein { from { opacity: 0 } to { opacity: 1 } }
          @keyframes pop { 0% { transform: scale(0.5); opacity: 0 } 60% { transform: scale(1.1); opacity: 1 } 100% { transform: scale(1) } }
        `}</style>
      </ScreenWrap>
    );
  }

  // view === 'playing'
  if (todayQs.length === 0) return <ScreenWrap><Spinner /></ScreenWrap>;
  const currentQ = todayQs[qIndex];
  if (!currentQ) return <ScreenWrap><Spinner /></ScreenWrap>;

  return (
    <div style={{ minHeight: '100vh', background: '#F4E8D8', padding: 20, fontFamily: 'Noto Sans TC, sans-serif' }}>
      {flash && (
        <div style={{ position: 'fixed', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', pointerEvents: 'none', zIndex: 100 }}>
          <img src={flash === 'right' ? '/level-assets/answer_right.webp' : '/level-assets/answer_wrong.webp'}
               alt="" style={{ width: '50%', maxWidth: 280, animation: 'flashIn 0.6s ease-out' }} />
        </div>
      )}
      <div style={{ maxWidth: 900, margin: '0 auto 16px', background: '#C57B57', color: 'white', padding: 16, borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <img src={`/level-assets/level_${tProg.unlockedLevel}.webp`} alt="" style={{ width: 36, height: 36, objectFit: 'contain' }} />
          <div>
            <div style={{ fontSize: '0.85rem', opacity: 0.9 }}>{topic.emoji} {topic.label} · Lv {tProg.unlockedLevel} {LEVEL_NAMES[tProg.unlockedLevel]}</div>
            <div style={{ fontSize: '1rem', fontWeight: 700 }}>第 {qIndex + 1} / {DAILY_QUESTIONS} 題</div>
          </div>
        </div>
        <button onClick={backToTopicSelect} style={{ background: 'rgba(255,255,255,0.2)', color: 'white', border: '1px solid rgba(255,255,255,0.4)', borderRadius: 8, padding: '8px 14px', fontSize: '0.85rem', cursor: 'pointer' }}>離開</button>
      </div>
      <div style={{ maxWidth: 900, margin: '0 auto 16px', display: 'flex', gap: 8 }}>
        {Array.from({ length: DAILY_QUESTIONS }).map((_, i) => {
          const r = tProg.todayResults[i];
          const bg = r === true ? '#4caf50' : r === false ? '#f44336' : i === qIndex ? '#C57B57' : '#e0d4be';
          return <div key={i} style={{ flex: 1, height: 8, borderRadius: 4, background: bg, transition: 'background 0.3s' }} />;
        })}
      </div>
      <div style={{ maxWidth: 900, margin: '0 auto', background: 'white', padding: 28, borderRadius: 12, boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
        <div style={{ marginBottom: 16 }}>
          <span style={{ background: '#8B4513', color: 'white', padding: '5px 14px', borderRadius: 14, fontSize: '0.85rem' }}>
            等級 {currentQ.level} • {topic.label}
          </span>
        </div>
        {currentQ.qimage_url && (
          <img src={currentQ.qimage_url} alt="題目圖" style={{ width: '100%', maxHeight: 360, objectFit: 'contain', borderRadius: 8, marginBottom: 18, background: '#fafafa' }} />
        )}
        <h2 style={{ fontSize: '1.4rem', marginBottom: 22, lineHeight: 1.6 }}>{currentQ.question}</h2>
        <div style={{ marginBottom: 18 }}>
          {currentQ.options.map((opt, i) => {
            const sel = selectedAnswer === i;
            const right = i === currentQ.correct_answer;
            let bg = '#fffaf5', col = '#1C1C1C';
            if (showExplanation) {
              if (right) { bg = '#4caf50'; col = 'white'; }
              else if (sel && !right) { bg = '#f44336'; col = 'white'; }
            } else if (sel) { bg = '#C57B57'; col = 'white'; }
            return (
              <button key={i} onClick={() => selectAnswer(i)} disabled={showExplanation}
                style={{ width: '100%', padding: 16, margin: '8px 0', background: bg, color: col, border: '2px solid #1C1C1C', borderRadius: 10, fontSize: '1.05rem', textAlign: 'left', cursor: showExplanation ? 'default' : 'pointer' }}>
                {String.fromCharCode(65 + i)}. {opt}
              </button>
            );
          })}
        </div>
        {showExplanation && (
          <div style={{ background: '#F4E8D8', padding: 18, borderRadius: 10, marginTop: 16, borderLeft: '5px solid #B85C38' }}>
            <h3 style={{ marginTop: 0 }}>💡 詳細解釋</h3>
            {currentQ.image_url && <img src={currentQ.image_url} alt="解釋圖" style={{ width: '100%', maxHeight: 280, objectFit: 'contain', borderRadius: 8, marginBottom: 12, background: '#fafafa' }} />}
            <p style={{ lineHeight: 1.6, margin: 0 }}>{currentQ.explanation}</p>
          </div>
        )}
        <div style={{ marginTop: 22, textAlign: 'center' }}>
          {!showExplanation ? (
            <button onClick={submitAnswer} disabled={selectedAnswer === null}
              style={{ ...primaryBtn(), background: selectedAnswer !== null ? '#C57B57' : '#ccc', cursor: selectedAnswer !== null ? 'pointer' : 'not-allowed' }}>
              ✓ 提交答案
            </button>
          ) : (
            <button onClick={nextOrFinish} style={primaryBtn()}>
              {qIndex < DAILY_QUESTIONS - 1 ? '➡️ 下一題' : '🏁 查看結果'}
            </button>
          )}
        </div>
      </div>
      <style jsx global>{`
        @keyframes flashIn { 0% { transform: scale(0.3); opacity: 0 } 40% { transform: scale(1.1); opacity: 1 } 100% { transform: scale(1); opacity: 0 } }
      `}</style>
    </div>
  );
}

// ============ Helpers / sub-components ============

function ScreenWrap({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 24, background: '#F4E8D8', fontFamily: 'Noto Sans TC, sans-serif' }}>
      {children}
    </div>
  );
}

function Card({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ background: 'white', borderRadius: 16, padding: 28, maxWidth: 480, width: '100%', boxShadow: '0 4px 16px rgba(0,0,0,0.08)' }}>{children}</div>
  );
}

function Spinner() {
  return (
    <div style={{ textAlign: 'center' }}>
      <h1 style={{ fontSize: '1.8rem' }}>🧠 解剖咬一口</h1>
      <p>載入中...</p>
      <div style={{ margin: '20px auto', width: 40, height: 40, border: '4px solid #f3f3f3', borderTop: '4px solid #C57B57', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
      <style jsx>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
    </div>
  );
}

function ErrorBox({ msg, onBack }: { msg: string; onBack: () => void }) {
  return (
    <Card>
      <h2 style={{ color: '#DC3545', marginTop: 0, textAlign: 'center' }}>⚠️ 載入失敗</h2>
      <p style={{ textAlign: 'center' }}>{msg}</p>
      <BackBtn onClick={onBack} />
    </Card>
  );
}

function BackBtn({ onClick }: { onClick: () => void }) {
  return (
    <button onClick={onClick} style={{ width: '100%', padding: 12, marginTop: 12, background: 'white', color: '#C57B57', border: '2px solid #C57B57', borderRadius: 10, fontSize: '1rem', cursor: 'pointer', fontWeight: 600 }}>
      ← 回題庫選擇
    </button>
  );
}

function ResetCountdown() {
  const [ms, setMs] = useState(msUntilTaipeiMidnight());
  useEffect(() => {
    const t = setInterval(() => setMs(msUntilTaipeiMidnight()), 60000);
    return () => clearInterval(t);
  }, []);
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  return <p style={{ color: '#999', fontSize: '0.9rem', textAlign: 'center', margin: '8px 0' }}>明日挑戰 {h} 小時 {m} 分鐘後重置</p>;
}

function cardBtn(): React.CSSProperties {
  return { background: 'white', border: '2px solid #C57B57', borderRadius: 14, padding: 18, cursor: 'pointer', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', transition: 'transform 0.2s, box-shadow 0.2s' };
}

function primaryBtn(): React.CSSProperties {
  return { padding: '14px 36px', background: '#C57B57', color: 'white', border: 'none', borderRadius: 10, fontSize: '1.05rem', cursor: 'pointer', fontWeight: 700, marginTop: 8 };
}
