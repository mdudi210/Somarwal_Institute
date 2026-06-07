import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Award,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  FileCheck2,
  GraduationCap,
  LayoutDashboard,
  LogIn,
  LogOut,
  Mail,
  MapPin,
  Menu,
  MessageCircle,
  MonitorCheck,
  Phone,
  RotateCcw,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  Users
} from "lucide-react";
import { api, clearSession, fallbackHome, getStoredUser, setSession } from "./api";
import "./styles.css";

function App() {
  const [route, setRoute] = useState(window.location.hash.replace("#", "") || "/");
  const [home, setHome] = useState(fallbackHome);
  const [toast, setToast] = useState("");
  const publicRoutes = ["/", "/courses", "/verify", "/typing"];

  useEffect(() => {
    const fetchHome = () => api("/api/home").then(setHome).catch(() => setHome(fallbackHome));
    const onHash = () => {
      setRoute(window.location.hash.replace("#", "") || "/");
      fetchHome();
    };
    window.addEventListener("hashchange", onHash);
    fetchHome();
    if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  const navigate = (next) => {
    const safeRoute = publicRoutes.includes(next) ? next : "/";
    window.location.hash = safeRoute;
    setRoute(safeRoute);
  };

  const notify = (message) => {
    setToast(message);
    window.setTimeout(() => setToast(""), 3500);
  };

  const page = useMemo(() => {
    if (route === "/typing") return <TypingPractice notify={notify} />;
    if (route === "/verify") return <VerifyCertificate notify={notify} />;
    if (route === "/courses") return <Courses courses={home.courses} />;
    return <PublicWebsite home={home} navigate={navigate} />;
  }, [route, home]);

  return (
    <>
      <Header navigate={navigate} />
      <main>{page}</main>
      <Footer />
      {toast && <div className="toast">{toast}</div>}
    </>
  );
}

function Header({ navigate }) {
  const [open, setOpen] = useState(false);
  const links = [
    ["Home", "/"],
    ["Courses", "/courses"],
    ["Typing Practice", "/typing"],
    ["Verify Certificate", "/verify"]
  ];
  return (
    <header className="topbar">
      <button className="brand" onClick={() => navigate("/")} aria-label="Somarwal home">
        <MonitorCheck size={28} />
        <span>Somarwal Institute</span>
      </button>
      <button className="icon-button menu-button" onClick={() => setOpen(!open)} aria-label="Menu">
        <Menu size={22} />
      </button>
      <nav className={open ? "nav open" : "nav"}>
        {links.map(([label, href]) => (
          <button key={href} onClick={() => navigate(href)}>{label}</button>
        ))}
        <button className="primary small" onClick={() => navigate("/verify")}><ShieldCheck size={17} /> Verify</button>
      </nav>
    </header>
  );
}

function PublicWebsite({ home, navigate }) {
  return (
    <>
      <section className="hero">
        <div className="hero-media" />
        <div className="hero-copy">
          <p className="eyebrow">Computer and Tech Training in Ajmer</p>
          <h1>Somarwal Computer & Tech Institute</h1>
          <p>Practical computer courses in Ajmer with a public certificate verification system for students, employers, and institutions.</p>
          <div className="hero-actions">
            <button className="primary" onClick={() => navigate("/verify")}>Verify Certificate <ChevronRight size={18} /></button>
            <button className="secondary" onClick={() => navigate("/courses")}>View Courses</button>
            <button className="secondary" onClick={() => navigate("/typing")}>Typing Practice</button>
            <a className="secondary" href="https://wa.me/919828272202">WhatsApp Us</a>
            <a className="secondary" href="tel:+919828272202">Call Now</a>
          </div>
        </div>
      </section>

      <section className="announcement-band">
        {(home.announcements || []).map((item) => (
          <article key={item.title}>
            <Sparkles size={22} />
            <div><strong>{item.title}</strong><span>{item.message}</span></div>
            <button onClick={() => navigate("/courses")}>View Courses</button>
          </article>
        ))}
      </section>

      <section className="stats">
        {Object.entries(home.stats).map(([label, value]) => (
          <div className="metric" key={label}>
            <strong>{value}</strong>
            <span>{label}</span>
          </div>
        ))}
      </section>

      <section className="section">
        <div className="section-title">
          <p className="eyebrow">Popular Programs</p>
          <h2>Courses built for practical outcomes</h2>
        </div>
        <CourseGrid courses={home.courses.slice(0, 6)} />
      </section>

      <section className="split-section">
        <div>
          <p className="eyebrow">Why Choose Us</p>
          <h2>Hands-on classes, digital records, and verifiable achievements</h2>
          <div className="feature-list">
            <Feature icon={BookOpen} title="Dynamic syllabus" text="Course modules, tools, fees, and career tracks can be managed from admin." />
            <Feature icon={FileCheck2} title="Digital certificates" text="Every certificate can be verified publicly using a secure certificate number." />
            <Feature icon={MessageCircle} title="Admission automation" text="Registration IDs, receipts, WhatsApp, and email flows are ready for integration." />
          </div>
        </div>
        <img className="side-image" src="https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80" alt="Students learning computers" />
      </section>

      <section className="typing-promo">
        <div>
          <p className="eyebrow">Typing Skill Builder</p>
          <h2>Practice speed and accuracy before your certificate exam</h2>
          <p>Timed tests, paragraph practice, custom text, live WPM, accuracy, errors, and saved local results.</p>
        </div>
        <button className="primary" onClick={() => navigate("/typing")}>Start Typing Practice</button>
      </section>

      <section className="section">
        <div className="section-title">
          <p className="eyebrow">Placements</p>
          <h2>Career progress from practical training</h2>
        </div>
        <div className="card-grid">
          {(home.placements || []).map((placement) => (
            <article className="card" key={placement.id}>
              <Award size={28} />
              <h3>{placement.student_name}</h3>
              <p>{placement.description || `${placement.course} student placed at ${placement.company}.`}</p>
              <strong>{placement.company}</strong>
              <span>{placement.package}</span>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-title">
          <p className="eyebrow">Gallery</p>
          <h2>Institute life and achievements</h2>
        </div>
        <div className="gallery-grid">
          {home.gallery.map((item) => (
            <article className="image-card" key={item.id}>
              <img src={item.image} alt={item.title} />
              <div><strong>{item.title}</strong><span>{item.category}</span></div>
            </article>
          ))}
        </div>
      </section>

      <section className="section testimonials">
        <div className="section-title">
          <p className="eyebrow">Student Reviews</p>
          <h2>Trusted by learners</h2>
        </div>
        <div className="card-grid">
          {home.reviews.map((review) => (
            <article className="card" key={review.id}>
              <div className="stars">{"★".repeat(review.rating || 5)}</div>
              <p>{review.message}</p>
              <strong>{review.student_name}</strong>
              <span>{review.course}</span>
            </article>
          ))}
        </div>
      </section>

      <section className="location-section">
        <div>
          <p className="eyebrow">Location</p>
          <h2>Visit Somarwal Institute, Ajmer</h2>
          <p>Use the map preview to plan your visit for admission, demo classes, or certificate support.</p>
        </div>
        <iframe title="Somarwal Institute Map" src="https://www.google.com/maps?q=Ajmer%20Rajasthan&output=embed" loading="lazy" />
      </section>
    </>
  );
}

function Feature({ icon: Icon, title, text }) {
  return <div className="feature"><Icon size={24} /><div><strong>{title}</strong><p>{text}</p></div></div>;
}

function About({ home }) {
  const about = home.about || {};
  return (
    <section className="page about-page">
      <div className="section-title">
        <p className="eyebrow">About Us</p>
        <h1>Practical computer education with discipline and guidance</h1>
      </div>
      <div className="about-grid">
        <article className="panel"><h2>Introduction</h2><p>Somarwal Computer & Tech Institute, Ajmer provides job-oriented computer, accounting, creative, AI, language, and coaching programs for students and professionals.</p></article>
        <article className="panel"><h2>Mission</h2><p>{about.mission}</p></article>
        <article className="panel"><h2>Vision</h2><p>{about.vision}</p></article>
        <article className="panel director-card"><img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=800&q=80" alt="Director" /><div><h2>Director's Message</h2><p>{about.director_message}</p></div></article>
      </div>
      <div className="section-title gallery-title"><p className="eyebrow">Team and Labs</p><h2>Learning spaces and faculty culture</h2></div>
      <div className="gallery-grid">
        <img className="side-image" src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1000&q=80" alt="Computer lab" />
        <img className="side-image" src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1000&q=80" alt="Faculty team" />
        <img className="side-image" src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1000&q=80" alt="Training session" />
      </div>
    </section>
  );
}

function Courses({ courses }) {
  return <section className="page section"><div className="section-title"><p className="eyebrow">Course Catalog</p><h1>All active courses</h1></div><CourseGrid courses={courses} /></section>;
}

function CourseGrid({ courses }) {
  return (
    <div className="course-grid">
      {courses.map((course) => (
        <article className="course-card" key={course.id}>
          <div className="course-top"><span>{course.category}</span><strong>Rs. {course.fees}</strong></div>
          <h3>{course.name}</h3>
          <p>{course.description}</p>
          <div className="chips"><span>{course.duration}</span><span>{course.code}</span></div>
          <ul>{(course.syllabus || []).slice(0, 4).map((item) => <li key={item}><CheckCircle2 size={16} /> {item}</li>)}</ul>
        </article>
      ))}
    </div>
  );
}

function CourseDetail({ course, navigate }) {
  if (!course) return <section className="page section"><h1>Course not found</h1></section>;
  return (
    <section className="page course-detail">
      <div>
        <p className="eyebrow">{course.category}</p>
        <h1>{course.name}</h1>
        <p>{course.description}</p>
        <div className="detail-meta"><span>{course.duration}</span><span>Rs. {course.fees}</span><span>{course.certificate_available ? "Certificate Included" : "Certificate Not Included"}</span></div>
        <button className="primary" onClick={() => navigate("/admission")}>Enroll in this course</button>
      </div>
      <div className="detail-panels">
        <article className="panel"><h2>Detailed Syllabus</h2><ul>{(course.syllabus || []).map((item) => <li key={item}>{item}</li>)}</ul></article>
        <article className="panel"><h2>Software Covered</h2><ul>{(course.software_covered || []).map((item) => <li key={item}>{item}</li>)}</ul></article>
        <article className="panel"><h2>Career Opportunities</h2><ul>{(course.career_options || []).map((item) => <li key={item}>{item}</li>)}</ul></article>
      </div>
    </section>
  );
}

const typingTextBank = {
  beginner: [
    "Computer practice builds confidence. Keep your fingers relaxed and type every word with steady attention.",
    "Digital skills help students complete forms, write letters, manage data, and communicate clearly.",
    "A good learner practices daily, checks mistakes, and improves speed step by step."
  ],
  intermediate: [
    "Typing accuracy matters more than rushing. When your hands follow rhythm, speed grows naturally and errors reduce.",
    "Office work often requires email writing, data entry, spreadsheet updates, and quick document preparation.",
    "Students who practice consistently can prepare better for exams, interviews, and computer operator roles."
  ],
  advanced: [
    "Professional typing requires focus, posture, punctuation control, number-row confidence, and quick correction awareness.",
    "Technology training connects practical software knowledge with disciplined habits, communication skills, and measurable progress.",
    "A certificate becomes more valuable when it represents real practice, verified performance, and dependable workplace readiness."
  ],
  numbers: [
    "Invoice 2045 includes 18 items, 3 discounts, GST 18 percent, and final payment of 12980 rupees.",
    "Batch 2026 starts on 08 June with 45 students, 6 modules, 12 tests, and 90 hours of practice.",
    "Receipt RCP20260012 shows fee 8500, paid 3000, pending 5500, and transaction number 582914706321."
  ]
};

const typingDurations = [60, 120, 180, 300];

function getTypingHistory() {
  try {
    return JSON.parse(localStorage.getItem("somarwal_typing_history") || "[]");
  } catch {
    return [];
  }
}

function saveTypingHistory(history) {
  localStorage.setItem("somarwal_typing_history", JSON.stringify(history.slice(0, 10)));
}

function createTypingText(level, mode, customText) {
  if (mode === "custom" && customText.trim().length >= 20) return customText.trim();
  const pool = typingTextBank[level] || typingTextBank.beginner;
  if (mode === "paragraph") return pool.join(" ");
  return pool[Math.floor(Math.random() * pool.length)];
}

function calculateTypingStats(input, target, elapsedSeconds) {
  const typedChars = input.length;
  let correctChars = 0;
  let errors = 0;
  for (let index = 0; index < typedChars; index += 1) {
    if (input[index] === target[index]) correctChars += 1;
    else errors += 1;
  }
  const minutes = Math.max(elapsedSeconds / 60, 1 / 60);
  const rawWpm = Math.round((typedChars / 5) / minutes);
  const wpm = Math.round((correctChars / 5) / minutes);
  const accuracy = typedChars ? Math.max(0, Math.round((correctChars / typedChars) * 100)) : 100;
  const cpm = Math.round(correctChars / minutes);
  return { typedChars, correctChars, errors, rawWpm, wpm, accuracy, cpm };
}

function TypingPractice({ notify }) {
  const [mode, setMode] = useState("timed");
  const [level, setLevel] = useState("beginner");
  const [duration, setDuration] = useState(60);
  const [customText, setCustomText] = useState("");
  const [target, setTarget] = useState(() => createTypingText("beginner", "timed", ""));
  const [input, setInput] = useState("");
  const [startedAt, setStartedAt] = useState(null);
  const [elapsed, setElapsed] = useState(0);
  const [finished, setFinished] = useState(false);
  const [history, setHistory] = useState(getTypingHistory);

  const stats = calculateTypingStats(input, target, elapsed);
  const timeLeft = mode === "timed" ? Math.max(duration - elapsed, 0) : null;
  const progress = target.length ? Math.min(100, Math.round((input.length / target.length) * 100)) : 0;
  const best = history.length ? Math.max(...history.map((item) => item.wpm)) : 0;

  useEffect(() => {
    if (!startedAt || finished) return undefined;
    const timer = window.setInterval(() => {
      const nextElapsed = Math.floor((Date.now() - startedAt) / 1000);
      setElapsed(nextElapsed);
      if ((mode === "timed" && nextElapsed >= duration) || input.length >= target.length) {
        setFinished(true);
      }
    }, 250);
    return () => window.clearInterval(timer);
  }, [startedAt, finished, duration, mode, input.length, target.length]);

  useEffect(() => {
    if (!finished || input.length === 0) return;
    const result = {
      id: Date.now(),
      mode,
      level,
      duration: mode === "timed" ? duration : elapsed,
      wpm: stats.wpm,
      rawWpm: stats.rawWpm,
      accuracy: stats.accuracy,
      errors: stats.errors,
      cpm: stats.cpm,
      created_at: new Date().toLocaleString()
    };
    setHistory((current) => {
      if (current[0]?.id === result.id) return current;
      const next = [result, ...current].slice(0, 10);
      saveTypingHistory(next);
      return next;
    });
  }, [finished]);

  const resetTest = (nextText = target) => {
    setTarget(nextText);
    setInput("");
    setStartedAt(null);
    setElapsed(0);
    setFinished(false);
  };

  const newText = () => resetTest(createTypingText(level, mode, customText));

  const updateMode = (nextMode) => {
    setMode(nextMode);
    resetTest(createTypingText(level, nextMode, customText));
  };

  const updateLevel = (nextLevel) => {
    setLevel(nextLevel);
    resetTest(createTypingText(nextLevel, mode, customText));
  };

  const handleTyping = (event) => {
    if (finished) return;
    const value = event.target.value;
    if (!startedAt && value.length > 0) setStartedAt(Date.now());
    setInput(value.slice(0, target.length));
    if (value.length >= target.length) setFinished(true);
  };

  const clearHistory = () => {
    setHistory([]);
    saveTypingHistory([]);
    notify("Typing history cleared");
  };

  return (
    <section className="page typing-page">
      <div className="typing-header">
        <div>
          <p className="eyebrow">Typing Practice</p>
          <h1>Speed, accuracy, and exam readiness</h1>
          <p>Practice English typing with live results and local progress history.</p>
        </div>
        <div className="typing-best"><Award size={24} /><span>Best WPM</span><strong>{best}</strong></div>
      </div>

      <div className="typing-shell">
        <aside className="typing-controls">
          <label>Mode</label>
          <div className="segmented">
            {["timed", "paragraph", "custom"].map((item) => <button key={item} className={mode === item ? "active" : ""} onClick={() => updateMode(item)}>{item}</button>)}
          </div>

          <label>Level</label>
          <select value={level} onChange={(event) => updateLevel(event.target.value)}>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
            <option value="numbers">Numbers</option>
          </select>

          {mode === "timed" && (
            <>
              <label>Duration</label>
              <div className="duration-grid">
                {typingDurations.map((seconds) => <button key={seconds} className={duration === seconds ? "active" : ""} onClick={() => { setDuration(seconds); resetTest(); }}>{seconds / 60} min</button>)}
              </div>
            </>
          )}

          {mode === "custom" && (
            <>
              <label>Custom text</label>
              <textarea value={customText} onChange={(event) => setCustomText(event.target.value)} placeholder="Paste at least 20 characters for a custom typing test." />
              <button className="secondary" onClick={newText}>Use Custom Text</button>
            </>
          )}

          <div className="typing-actions">
            <button className="primary" onClick={newText}><Sparkles size={18} /> New Text</button>
            <button className="secondary" onClick={() => resetTest()}><RotateCcw size={18} /> Restart</button>
          </div>
        </aside>

        <div className="typing-workspace">
          <div className="typing-stat-grid">
            <TypingStat label="WPM" value={stats.wpm} />
            <TypingStat label="Accuracy" value={`${stats.accuracy}%`} />
            <TypingStat label="Errors" value={stats.errors} />
            <TypingStat label={mode === "timed" ? "Time Left" : "Time"} value={mode === "timed" ? `${timeLeft}s` : `${elapsed}s`} />
            <TypingStat label="CPM" value={stats.cpm} />
            <TypingStat label="Progress" value={`${progress}%`} />
          </div>

          <div className="typing-progress"><span style={{ width: `${progress}%` }} /></div>

          <div className="typing-text" aria-label="Typing text">
            {target.split("").map((char, index) => {
              const typed = input[index];
              const className = typed == null ? "" : typed === char ? "correct" : "wrong";
              return <span key={`${char}-${index}`} className={className}>{char === " " ? "\u00a0" : char}</span>;
            })}
          </div>

          <textarea
            className="typing-input"
            value={input}
            onChange={handleTyping}
            disabled={finished}
            autoFocus
            placeholder="Start typing here..."
          />

          {finished && (
            <div className="result-panel">
              <ShieldCheck size={30} />
              <div>
                <h2>Test Complete</h2>
                <p>{stats.wpm} WPM, {stats.accuracy}% accuracy, {stats.errors} errors, {stats.rawWpm} raw WPM.</p>
              </div>
              <button className="primary" onClick={newText}>Practice Again</button>
            </div>
          )}
        </div>
      </div>

      <section className="typing-history">
        <div className="section-title">
          <p className="eyebrow">Progress</p>
          <h2>Recent typing results</h2>
        </div>
        <div className="table-panel">
          <div className="history-toolbar">
            <strong>{history.length} saved results</strong>
            <button className="secondary small" onClick={clearHistory}>Clear History</button>
          </div>
          <div className="table-scroll">
            <table>
              <thead><tr><th>Date</th><th>Mode</th><th>Level</th><th>WPM</th><th>Accuracy</th><th>Errors</th><th>Time</th></tr></thead>
              <tbody>
                {history.length === 0 && <tr><td colSpan="7">No results yet</td></tr>}
                {history.map((item) => (
                  <tr key={item.id}>
                    <td>{item.created_at}</td>
                    <td>{item.mode}</td>
                    <td>{item.level}</td>
                    <td>{item.wpm}</td>
                    <td>{item.accuracy}%</td>
                    <td>{item.errors}</td>
                    <td>{item.duration}s</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </section>
  );
}

function TypingStat({ label, value }) {
  return <div className="typing-stat"><span>{label}</span><strong>{value}</strong></div>;
}

function Enquiry({ courses, notify }) {
  const [form, setForm] = useState({ name: "", phone: "", email: "", course_interest: courses[0]?.name || "", comments_questions: "", preferred_time: "", preferred_mode: "Phone" });
  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value });
  const submit = async (event) => {
    event.preventDefault();
    try {
      await api("/api/enquiries", { method: "POST", body: JSON.stringify(form) });
      notify("Enquiry submitted successfully. We will contact you soon!");
      setForm({ name: "", phone: "", email: "", course_interest: courses[0]?.name || "", comments_questions: "", preferred_time: "", preferred_mode: "Phone" });
    } catch (error) {
      notify(error.message);
    }
  };
  return (
    <section className="page form-layout">
      <div>
        <p className="eyebrow">Contact Us</p>
        <h1>Make an Enquiry</h1>
        <p>Have questions about our courses or batches? Send us an enquiry and we'll get back to you.</p>
      </div>
      <form className="panel" onSubmit={submit}>
        <input name="name" placeholder="Full name" value={form.name} onChange={update} required />
        <input name="phone" placeholder="Mobile number" value={form.phone} onChange={update} required />
        <input name="email" type="email" placeholder="Email (optional)" value={form.email} onChange={update} />
        <select name="course_interest" value={form.course_interest} onChange={update}>{courses.map((course) => <option key={course.code} value={course.name}>{course.name}</option>)}</select>
        <textarea name="comments_questions" placeholder="Your questions or comments" value={form.comments_questions} onChange={update} required />
        <input name="preferred_time" placeholder="Preferred time to connect (e.g. 5 PM - 6 PM)" value={form.preferred_time} onChange={update} />
        <select name="preferred_mode" value={form.preferred_mode} onChange={update}>
          <option value="Phone">Phone Call</option>
          <option value="WhatsApp">WhatsApp Chat</option>
          <option value="Email">Email</option>
        </select>
        <button className="primary" type="submit"><Send size={18} /> Submit Enquiry</button>
      </form>
    </section>
  );
}

function Admission({ courses, notify, user, navigate }) {
  if (!user) {
    return (
      <section className="page form-layout">
        <div>
          <p className="eyebrow">Online Admission</p>
          <h1>Login Required</h1>
          <p>You must have an account and be logged in to apply for admission. If you just want to make an enquiry, please use the Enquiry form.</p>
          <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
            <button className="primary" onClick={() => navigate("/login")}>Login / Register</button>
            <button className="secondary" onClick={() => navigate("/enquiry")}>Submit Enquiry Instead</button>
          </div>
        </div>
      </section>
    );
  }

  const [form, setForm] = useState({ name: user.name || "", father: "", dob: "", phone: user.phone || "", email: user.email || "", school_name: "", qualification: "", address: "", course: courses[0]?.code || "DCA", batch_id: "", paid_amount: 1000, payment_mode: "UPI", transaction_id: "", otp_code: "" });
  const [batches, setBatches] = useState([]);
  const [receipt, setReceipt] = useState(null);
  
  useEffect(() => {
    if (form.course) {
      api(`/api/courses/${form.course}/batches`)
        .then(data => {
          setBatches(data);
          if (data.length > 0) setForm(f => ({ ...f, batch_id: data[0].id }));
          else setForm(f => ({ ...f, batch_id: "" }));
        })
        .catch(err => notify(err.message));
    }
  }, [form.course]);

  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value });

  const submit = async (event) => {
    event.preventDefault();
    if (form.payment_mode === "UPI" && (!form.transaction_id || form.transaction_id.length !== 12)) {
      notify("Please enter a valid 12-digit UPI transaction ID");
      return;
    }
    if (!form.batch_id) {
      notify("Please select a batch");
      return;
    }
    try {
      const payload = { ...form, paid_amount: Number(form.paid_amount), batch_id: Number(form.batch_id) };
      if (!payload.email) payload.email = null;
      if (!payload.transaction_id) payload.transaction_id = null;
      if (!payload.otp_code) payload.otp_code = null;
      
      const data = await api("/api/admission/apply", { method: "POST", body: JSON.stringify(payload) });
      setReceipt(data);
      notify("Admission submitted successfully");
    } catch (error) {
      notify(error.message);
    }
  };
  return (
    <section className="page form-layout">
      <div>
        <p className="eyebrow">Online Admission</p>
        <h1>Apply for a course</h1>
        <p>Submit student details and create a registration record with receipt tracking.</p>
        {receipt && <div className="success-box"><ShieldCheck size={28} /><strong>{receipt.registration_no}</strong><span>Receipt: {receipt.receipt}</span><span>PDF: {receipt.receipt_url}</span><span>Email: {receipt.email_notification}</span><span>WhatsApp: {receipt.whatsapp_notification}</span><span>Pending: Rs. {receipt.pending_amount}</span></div>}
      </div>
      <form className="panel" onSubmit={submit}>
        <input name="name" placeholder="Student name" value={form.name} onChange={update} required />
        <input name="father" placeholder="Father name" value={form.father} onChange={update} required />
        <input name="dob" type="date" value={form.dob} onChange={update} required />
        
        <input name="phone" placeholder="Mobile number" value={form.phone} onChange={update} required />

        <input name="email" type="email" placeholder="Email" value={form.email} readOnly style={{ opacity: 0.7, cursor: "not-allowed" }} />
        
        <label>Course</label>
        <select name="course" value={form.course} onChange={update}>{courses.map((course) => <option key={course.code} value={course.code}>{course.name}</option>)}</select>
        
        <label>Batch</label>
        <select name="batch_id" value={form.batch_id} onChange={update} required>
          {batches.length === 0 && <option value="">No batches available</option>}
          {batches.map((batch) => <option key={batch.id} value={batch.id}>{batch.batch_no} ({new Date(batch.start_date).toLocaleDateString()})</option>)}
        </select>

        <input name="school_name" placeholder="School / College name" value={form.school_name} onChange={update} />
        <input name="qualification" placeholder="Qualification" value={form.qualification} onChange={update} />
        <textarea name="address" placeholder="Address" value={form.address} onChange={update} />
        <select name="payment_mode" value={form.payment_mode} onChange={update}><option value="UPI">UPI</option><option value="CASH">Cash</option><option value="CARD">Card</option><option value="NETBANKING">NetBanking</option></select>
        <input name="paid_amount" type="number" min="1000" placeholder="Paid amount" value={form.paid_amount} onChange={update} required />
        
        {form.payment_mode === "UPI" && form.paid_amount >= 1000 && (
          <div className="qr-box" style={{ textAlign: "center", margin: "1rem 0", padding: "1rem", border: "1px dashed var(--border)" }}>
            <p style={{ marginBottom: "0.5rem", fontWeight: "bold" }}>Scan to pay Rs. {form.paid_amount}</p>
            <img src={`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa=somarwal@upi&pn=SomarwalInstitute&am=${form.paid_amount}`} alt="UPI QR Code" style={{ display: "inline-block", marginBottom: "1rem" }} />
            <input name="transaction_id" placeholder="12-digit UPI Transaction ID" value={form.transaction_id} onChange={update} required pattern="\d{12}" maxLength="12" />
          </div>
        )}
        <button className="primary" type="submit"><Send size={18} /> Submit Admission</button>
      </form>
    </section>
  );
}

function VerifyCertificate({ notify }) {
  const [certificateNo, setCertificateNo] = useState("CERT1001");
  const [result, setResult] = useState(null);
  const verify = async (event) => {
    event.preventDefault();
    try {
      setResult(await api(`/api/certificate/verify/${certificateNo}`));
    } catch (error) {
      notify(error.message);
    }
  };
  return (
    <section className="page verify-layout">
      <div>
        <p className="eyebrow">Certificate Verification</p>
        <h1>Check authenticity instantly</h1>
        <p>Enter certificate number or scan a QR-linked certificate page to validate the record.</p>
        <form className="search-box" onSubmit={verify}>
          <Search size={20} />
          <input value={certificateNo} onChange={(event) => setCertificateNo(event.target.value)} placeholder="Certificate number" />
          <button className="primary" type="submit">Verify</button>
        </form>
      </div>
      {result && <div className={result.verified ? "verify-card verified" : "verify-card rejected"}>
        {result.verified ? <ShieldCheck size={36} /> : <FileCheck2 size={36} />}
        <h2>{result.verified ? "Verified By Somarwal Institute" : "Fake Certificate Detected"}</h2>
        {result.verified ? <><p>{result.student}</p><span>{result.course}</span><span>Grade {result.grade} | {result.percentage}%</span></> : <p>{result.message}</p>}
      </div>}
    </section>
  );
}

function Login({ setUser, navigate, notify }) {
  const [form, setForm] = useState({ email: "admin@somarwal.edu", password: "admin123456" });
  const submit = async (event) => {
    event.preventDefault();
    try {
      const session = await api("/api/auth/login", { method: "POST", body: JSON.stringify(form) });
      setSession(session);
      setUser({ name: session.name, role: session.role, email: session.email, phone: session.phone });
      notify(`Welcome ${session.name}`);
      navigate(session.role === "STUDENT" ? "/student" : "/admin");
    } catch (error) {
      notify(error.message);
    }
  };
  return (
    <section className="page login-page">
      <form className="login-card" onSubmit={submit}>
        <LayoutDashboard size={34} />
        <h1>Institute Login</h1>
        <input type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} placeholder="Email" required />
        <input type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} placeholder="Password" required />
        <button className="primary" type="submit"><LogIn size={18} /> Sign In</button>
        <p>Don't have an account? <a href="#/register">Register</a></p>
        <p>Admin: admin@somarwal.edu / admin123456</p>
        <p>Student: student@somarwal.edu / student123456</p>
      </form>
    </section>
  );
}

function Register({ navigate, notify }) {
  const [form, setForm] = useState({ name: "", email: "", phone: "", password: "", role: "STUDENT" });
  
  const submitDetails = async (event) => {
    event.preventDefault();
    try {
      await api("/api/auth/register", { method: "POST", body: JSON.stringify(form) });
      notify("Registration successful! Please login.");
      navigate("/login");
    } catch (error) {
      notify(error.message);
    }
  };

  return (
    <section className="page login-page">
      <form className="login-card" onSubmit={submitDetails}>
        <LayoutDashboard size={34} />
        <h1>Student Registration</h1>
        <input type="text" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Full Name" required />
        <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="Email Address" required />
        <input type="text" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} placeholder="Phone Number" required />
        <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="Password" required minLength="6" />
        <button className="primary" type="submit"><LogIn size={18} /> Register</button>
        <p>Already have an account? <a href="#/login">Sign In</a></p>
      </form>
    </section>
  );
}

function AdminStudentProfile({ navigate, notify }) {
  const [data, setData] = useState(null);
  const [certForm, setCertForm] = useState({ grade: "A", percentage: 90, certificate_no: "" });
  const [showCertForm, setShowCertForm] = useState(false);
  const [editingCert, setEditingCert] = useState(null);
  const studentId = window.location.hash.split("/").pop();

  useEffect(() => {
    api(`/api/admin/students/${studentId}`).then(setData).catch((err) => notify(err.message));
  }, [studentId]);

  const requestPayment = async () => {
    try {
      const res = await api(`/api/admin/students/${studentId}/request-payment`, { method: "POST" });
      notify(res.message);
    } catch (err) {
      notify(err.message);
    }
  };

  const handleFeeStatus = async (feeId, status) => {
    try {
      await api(`/api/admin/fees/${feeId}/status`, { method: "PUT", body: JSON.stringify({ status }) });
      notify("Fee status updated. Bank match verified.");
      api(`/api/admin/students/${studentId}`).then(setData);
    } catch (error) {
      notify(error.message);
    }
  };

  const issueCertificate = async (e) => {
    e.preventDefault();
    try {
      const body = { student_id: Number(studentId), course_id: data.course.id, grade: certForm.grade, percentage: Number(certForm.percentage) };
      if (certForm.certificate_no) body.certificate_no = certForm.certificate_no;
      
      const res = await api("/api/admin/certificate/create", { method: "POST", body: JSON.stringify(body) });
      notify("Certificate issued: " + res.certificate_no);
      setShowCertForm(false);
      setCertForm({ grade: "A", percentage: 90, certificate_no: "" });
      api(`/api/admin/students/${studentId}`).then(setData);
    } catch (err) {
      notify(err.message);
    }
  };

  const updateCertificate = async (e) => {
    e.preventDefault();
    try {
      await api(`/api/admin/certificate/${editingCert.id}`, { method: "PUT", body: JSON.stringify({ grade: certForm.grade, percentage: Number(certForm.percentage), certificate_no: certForm.certificate_no || undefined }) });
      notify("Certificate updated");
      setEditingCert(null);
      setShowCertForm(false);
      setCertForm({ grade: "A", percentage: 90, certificate_no: "" });
      api(`/api/admin/students/${studentId}`).then(setData);
    } catch (err) {
      notify(err.message);
    }
  };

  if (!data) return <section className="page section"><h1>Loading...</h1></section>;

  const paymentsWithActions = data.fees.map((p) => ({
    ...p,
    approval: p.status === "PENDING" ? (
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <button className="primary small" onClick={() => handleFeeStatus(p.id, "APPROVED")}>Verify & Approve</button>
        <button className="secondary small" onClick={() => handleFeeStatus(p.id, "REJECTED")}>Reject</button>
      </div>
    ) : (
      <strong>{p.status}</strong>
    )
  }));
  
  const certificatesWithActions = data.certificates.map(c => ({
    ...c,
    actions: <button className="secondary small" onClick={() => { setEditingCert(c); setCertForm({ grade: c.grade, percentage: c.percentage, certificate_no: c.certificate_no }); setShowCertForm(true); }}>Edit</button>
  }));

  return (
    <section className="page dashboard">
      <button className="secondary small" onClick={() => navigate("/admin")} style={{ marginBottom: "1rem" }}>&larr; Back to Dashboard</button>
      <div className="section-title">
        <p className="eyebrow">Student Profile</p>
        <h1>{data.profile.student_name} ({data.profile.registration_no})</h1>
      </div>
      
      <div className="student-summary">
        <Feature icon={GraduationCap} title={data.course?.name || "No Course"} text={`Phone: ${data.profile.phone}`} />
        <Feature icon={Award} title="Certificates" text={`${data.certificates.length} Issued`} />
        <Feature icon={ShieldCheck} title="Financials" text={`Paid: ${data.financials.total_paid} | Pending: ${data.financials.pending_amount}`} />
      </div>

      {data.financials.pending_amount > 0 && (
        <div className="panel" style={{ marginBottom: "2rem", borderLeft: "4px solid var(--accent)", background: "var(--surface)" }}>
          <h3 style={{ margin: "0 0 0.5rem 0" }}>Pending Fees: Rs. {data.financials.pending_amount}</h3>
          <p style={{ margin: "0 0 1rem 0" }}>This student has unpaid fees. Send a reminder to their WhatsApp and Email.</p>
          <button className="primary" onClick={requestPayment}>Request Payment via WhatsApp/Email</button>
        </div>
      )}

      {showCertForm ? (
        <form className="panel" onSubmit={editingCert ? updateCertificate : issueCertificate} style={{ marginBottom: "2rem", borderLeft: "4px solid var(--accent)", background: "var(--surface)" }}>
          <h3 style={{ margin: "0 0 0.5rem 0" }}>{editingCert ? "Update Certificate" : "Issue Certificate"}</h3>
          <input name="certificate_no" placeholder="Certificate ID (Leave blank to auto-generate)" value={certForm.certificate_no} onChange={(e) => setCertForm({...certForm, certificate_no: e.target.value})} />
          <input name="grade" placeholder="Grade (e.g. A, B+)" value={certForm.grade} onChange={(e) => setCertForm({...certForm, grade: e.target.value})} required />
          <input name="percentage" type="number" min="0" max="100" placeholder="Percentage" value={certForm.percentage} onChange={(e) => setCertForm({...certForm, percentage: e.target.value})} required />
          <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
            <button className="primary" type="submit">{editingCert ? "Save Changes" : "Generate Certificate"}</button>
            <button className="secondary" type="button" onClick={() => { setShowCertForm(false); setEditingCert(null); setCertForm({ grade: "A", percentage: 90, certificate_no: "" }); }}>Cancel</button>
          </div>
        </form>
      ) : (
        <div style={{ marginBottom: "2rem" }}>
          <button className="primary" onClick={() => setShowCertForm(true)}>+ Issue Certificate</button>
        </div>
      )}

      <div className="dashboard-grid">
        <Table title="Payment History" rows={paymentsWithActions} cols={["receipt_no", "paid_amount", "pending_amount", "payment_mode", "transaction_id", "approval"]} />
        <Table title="Certificates" rows={certificatesWithActions} cols={["certificate_no", "grade", "percentage", "issue_date", "actions"]} />
      </div>
    </section>
  );
}

function AdminPortal({ courses, navigate, notify }) {
  const [data, setData] = useState(null);
  const [showAdmissionForm, setShowAdmissionForm] = useState(false);
  const [showCourseManager, setShowCourseManager] = useState(false);
  const [showStudentManager, setShowStudentManager] = useState(false);
  const [showBatchManager, setShowBatchManager] = useState(false);

  const loadData = () => {
    api("/api/admin/dashboard").then(setData).catch((error) => notify(error.message));
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleFeeStatus = async (feeId, status) => {
    try {
      await api(`/api/admin/fees/${feeId}/status`, { method: "PUT", body: JSON.stringify({ status }) });
      notify("Fee status updated");
      loadData();
    } catch (error) {
      notify(error.message);
    }
  };

  if (!data) return <section className="page section"><h1>Loading admin dashboard...</h1></section>;

  if (showAdmissionForm) {
    return (
      <section className="page dashboard">
        <div className="section-title">
          <p className="eyebrow">Admin Action</p>
          <h1>New Admission</h1>
          <button className="secondary" onClick={() => setShowAdmissionForm(false)}>Back to Dashboard</button>
        </div>
        <Admission courses={courses} notify={notify} />
      </section>
    );
  }

  if (showCourseManager) {
    return (
      <section className="page dashboard">
        <div className="section-title">
          <p className="eyebrow">Admin Action</p>
          <h1>Course Management</h1>
          <button className="secondary" onClick={() => setShowCourseManager(false)}>Back to Dashboard</button>
        </div>
        <CourseManager notify={notify} />
      </section>
    );
  }

  if (showStudentManager) {
    return (
      <section className="page dashboard">
        <div className="section-title">
          <p className="eyebrow">Admin Action</p>
          <h1>Student Management</h1>
          <button className="secondary" onClick={() => setShowStudentManager(false)}>Back to Dashboard</button>
        </div>
        <StudentManager navigate={navigate} notify={notify} />
      </section>
    );
  }

  if (showBatchManager) {
    return (
      <section className="page dashboard">
        <div className="section-title">
          <p className="eyebrow">Admin Action</p>
          <h1>Batch Management</h1>
          <button className="secondary" onClick={() => setShowBatchManager(false)}>Back to Dashboard</button>
        </div>
        <BatchManager courses={courses} notify={notify} />
      </section>
    );
  }

  const paymentsWithActions = data.payments.map((p) => ({
    ...p,
    approval: p.status === "PENDING" ? (
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <button className="primary small" onClick={() => handleFeeStatus(p.id, "APPROVED")}>Yes</button>
        <button className="secondary small" onClick={() => handleFeeStatus(p.id, "REJECTED")}>No</button>
      </div>
    ) : (
      <strong>{p.status}</strong>
    )
  }));

  return (
    <section className="page dashboard">
      <div className="section-title">
        <p className="eyebrow">Admin Control Panel</p>
        <h1>Operations dashboard</h1>
        <div style={{ display: "flex", gap: "1rem" }}>
          <button className="primary" onClick={() => setShowAdmissionForm(true)}>+ Add Admission</button>
          <button className="secondary" onClick={() => setShowStudentManager(true)}>Manage Students</button>
          <button className="secondary" onClick={() => setShowCourseManager(true)}>Manage Courses</button>
          <button className="secondary" onClick={() => setShowBatchManager(true)}>Manage Batches</button>
        </div>
      </div>
      <div className="stats">
        {Object.entries(data.metrics).map(([label, value]) => <div className="metric" key={label}><strong>{value}</strong><span>{label}</span></div>)}
      </div>
      <div className="dashboard-list">
        <Table title="Recent Admissions" rows={data.students.map((s) => ({ ...s, registration_no: <button style={{ padding: 0, border: 'none', background: 'none', color: 'var(--accent)', cursor: 'pointer', textDecoration: 'underline' }} onClick={() => navigate(`/admin/student/${s.id}`)}>{s.registration_no}</button> }))} cols={["registration_no", "student_name", "phone", "course_name", "receipt_no", "status"]} />
        <Table title="New Enquiries" rows={data.enquiries} cols={["name", "phone", "course_interest", "preferred_mode", "status"]} />
        <Table title="Payments" rows={paymentsWithActions} cols={["receipt_no", "registration_no", "course_name", "paid_amount", "pending_amount", "payment_mode", "approval"]} />
        <Table title="Automation Logs" rows={data.notifications} cols={["title", "receiver", "send_type", "status"]} />
      </div>
    </section>
  );
}

function StudentManager({ navigate, notify }) {
  const [students, setStudents] = useState([]);
  
  useEffect(() => {
    api("/api/admin/students").then(setStudents).catch((err) => notify(err.message));
  }, []);

  const studentsWithLinks = students.map((s) => ({
    ...s,
    registration_no: <button style={{ padding: 0, border: 'none', background: 'none', color: 'var(--accent)', cursor: 'pointer', textDecoration: 'underline' }} onClick={() => navigate(`/admin/student/${s.id}`)}>{s.registration_no}</button>,
    course_name: s.course ? s.course.name : "-",
  }));

  return (
    <div className="dashboard-list">
      <Table title="All Students" rows={studentsWithLinks} cols={["registration_no", "student_name", "phone", "course_name", "status"]} />
    </div>
  );
}

function BatchManager({ courses, notify }) {
  const [batches, setBatches] = useState([]);
  const [form, setForm] = useState({ course_id: courses[0]?.id || "", batch_no: "", start_date: "", end_date: "", status: "UPCOMING" });
  
  const loadBatches = () => {
    api("/api/admin/batches").then(setBatches).catch((err) => notify(err.message));
  };
  
  useEffect(() => { loadBatches(); }, []);

  const submit = async (e) => {
    e.preventDefault();
    try {
      await api("/api/admin/batches", { method: "POST", body: JSON.stringify({ ...form, course_id: Number(form.course_id) }) });
      notify("Batch created successfully");
      loadBatches();
      setForm({ course_id: courses[0]?.id || "", batch_no: "", start_date: "", end_date: "", status: "UPCOMING" });
    } catch (err) {
      notify(err.message);
    }
  };

  const batchesWithActions = batches.map(b => ({
    ...b,
    course_name: courses.find(c => c.id === b.course_id)?.name || "-",
    actions: (
      <select value={b.status} onChange={async (e) => {
        try {
          await api(`/api/admin/batches/${b.id}`, { method: "PUT", body: JSON.stringify({ status: e.target.value }) });
          notify("Batch status updated");
          loadBatches();
        } catch (err) { notify(err.message); }
      }}>
        <option value="UPCOMING">UPCOMING</option>
        <option value="ACTIVE">ACTIVE</option>
        <option value="COMPLETED">COMPLETED</option>
      </select>
    )
  }));

  return (
    <div className="dashboard-list">
      <form className="panel" onSubmit={submit} style={{ marginBottom: "2rem" }}>
        <h3>Create New Batch</h3>
        <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <select value={form.course_id} onChange={e => setForm({...form, course_id: e.target.value})} required>
            {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
          <input placeholder="Batch Number/Name" value={form.batch_no} onChange={e => setForm({...form, batch_no: e.target.value})} required />
          <input type="date" value={form.start_date} onChange={e => setForm({...form, start_date: e.target.value})} required />
          <input type="date" value={form.end_date} onChange={e => setForm({...form, end_date: e.target.value})} required />
          <button className="primary" type="submit">Create Batch</button>
        </div>
      </form>
      <Table title="Existing Batches" rows={batchesWithActions} cols={["batch_no", "course_name", "start_date", "end_date", "status", "actions"]} />
    </div>
  );
}

function CourseManager({ notify }) {
  const [courses, setCourses] = useState([]);
  const [editingCourse, setEditingCourse] = useState(null);

  const loadCourses = () => {
    api("/api/admin/courses").then(setCourses).catch((err) => notify(err.message));
  };

  useEffect(() => { loadCourses(); }, []);

  const hideCourse = async (id) => {
    try {
      await api(`/api/admin/courses/${id}`, { method: "DELETE" });
      notify("Course hidden successfully");
      loadCourses();
    } catch (err) {
      notify(err.message);
    }
  };

  if (editingCourse) {
    return <CourseForm course={editingCourse === true ? {} : editingCourse} onSave={() => { setEditingCourse(null); loadCourses(); }} onCancel={() => setEditingCourse(null)} notify={notify} />;
  }

  const coursesWithActions = courses.map((c) => ({
    ...c,
    status: c.status ? "Active" : "Hidden",
    actions: (
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <button className="secondary small" onClick={() => setEditingCourse(c)}>Edit</button>
        {c.status && <button className="secondary small" onClick={() => hideCourse(c.id)}>Hide</button>}
      </div>
    )
  }));

  return (
    <div>
      <div style={{ marginBottom: "1rem" }}>
        <button className="primary" onClick={() => setEditingCourse(true)}>+ Add New Course</button>
      </div>
      <Table title="All Courses" rows={coursesWithActions} cols={["code", "name", "category", "fees", "status", "actions"]} />
    </div>
  );
}

function CourseForm({ course, onSave, onCancel, notify }) {
  const [form, setForm] = useState({
    name: course.name || "",
    code: course.code || "",
    category: course.category || "",
    duration: course.duration || "",
    fees: course.fees || 0,
    description: course.description || "",
    syllabus: (course.syllabus || []).join(", "),
    software_covered: (course.software_covered || []).join(", "),
    career_options: (course.career_options || []).join(", "),
    certificate_available: course.certificate_available ?? true,
    status: course.status ?? true,
  });

  const update = (e) => {
    const value = e.target.type === "checkbox" ? e.target.checked : e.target.value;
    setForm({ ...form, [e.target.name]: value });
  };

  const submit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...form,
        fees: Number(form.fees),
        syllabus: form.syllabus.split(",").map(s => s.trim()).filter(Boolean),
        software_covered: form.software_covered.split(",").map(s => s.trim()).filter(Boolean),
        career_options: form.career_options.split(",").map(s => s.trim()).filter(Boolean),
      };
      if (course.id) {
        await api(`/api/admin/courses/${course.id}`, { method: "PUT", body: JSON.stringify(payload) });
        notify("Course updated successfully");
      } else {
        await api("/api/admin/courses", { method: "POST", body: JSON.stringify(payload) });
        notify("Course created successfully");
      }
      onSave();
    } catch (err) {
      notify(err.message);
    }
  };

  return (
    <form className="panel" onSubmit={submit}>
      <h2>{course.id ? "Edit Course" : "Add Course"}</h2>
      <input name="name" placeholder="Course Name" value={form.name} onChange={update} required />
      <input name="code" placeholder="Course Code" value={form.code} onChange={update} required />
      <input name="category" placeholder="Category" value={form.category} onChange={update} required />
      <input name="duration" placeholder="Duration (e.g. 3 Months)" value={form.duration} onChange={update} required />
      <input name="fees" type="number" min="0" placeholder="Fees" value={form.fees} onChange={update} required />
      <textarea name="description" placeholder="Description" value={form.description} onChange={update} required />
      
      <p style={{ marginTop: "1rem" }}>Comma-separated lists:</p>
      <input name="syllabus" placeholder="Syllabus (e.g. Intro, Variables, Loops)" value={form.syllabus} onChange={update} />
      <input name="software_covered" placeholder="Software (e.g. VS Code, Excel)" value={form.software_covered} onChange={update} />
      <input name="career_options" placeholder="Career Options (e.g. Web Dev, Accountant)" value={form.career_options} onChange={update} />
      
      <div style={{ margin: "1rem 0", display: "flex", gap: "1rem" }}>
        <label><input type="checkbox" name="certificate_available" checked={form.certificate_available} onChange={update} /> Certificate Available</label>
        <label><input type="checkbox" name="status" checked={form.status} onChange={update} /> Active</label>
      </div>

      <div style={{ display: "flex", gap: "1rem" }}>
        <button className="primary" type="submit">Save Course</button>
        <button className="secondary" type="button" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  );
}

function StudentPortal({ notify }) {
  const [data, setData] = useState(null);
  const [showPay, setShowPay] = useState(false);
  const [payForm, setPayForm] = useState({ paid_amount: "", transaction_id: "", payment_mode: "UPI" });

  const loadData = () => {
    api("/api/student/dashboard").then(setData).catch((error) => notify(error.message));
  };

  useEffect(() => { loadData(); }, []);

  const submitPayment = async (e) => {
    e.preventDefault();
    try {
      await api("/api/student/fees/pay-remaining", { method: "POST", body: JSON.stringify(payForm) });
      notify("Payment details submitted for verification.");
      setShowPay(false);
      loadData();
    } catch (err) {
      notify(err.message);
    }
  };

  if (!data) return <section className="page section"><h1>Loading student portal...</h1></section>;

  const totalPaid = data.fees.filter(f => f.status === "APPROVED").reduce((sum, f) => sum + f.paid_amount, 0);
  const pendingAmount = Math.max((data.course?.fees || 0) - totalPaid, 0);

  return (
    <section className="page dashboard">
      <div className="section-title"><p className="eyebrow">Student PWA</p><h1>{data.profile.student_name}</h1></div>
      <div className="student-summary">
        <Feature icon={GraduationCap} title={data.course.name} text={`Registration ${data.profile.registration_no}`} />
        <Feature icon={Award} title="Certificate" text={data.certificates[0]?.certificate_no || "In progress"} />
        <Feature icon={Users} title="Attendance" text={`${data.attendance.present} present classes`} />
      </div>

      {pendingAmount > 0 && !showPay && (
        <div className="panel" style={{ marginBottom: "2rem", borderLeft: "4px solid var(--accent)", background: "var(--surface)" }}>
          <h3 style={{ margin: "0 0 0.5rem 0" }}>Pending Fees: Rs. {pendingAmount}</h3>
          <p style={{ margin: "0 0 1rem 0" }}>You have an outstanding balance. Please clear your dues to receive your certificate.</p>
          <button className="primary" onClick={() => setShowPay(true)}>Pay Remaining Amount</button>
        </div>
      )}

      {showPay && (
        <form className="panel" onSubmit={submitPayment} style={{ marginBottom: "2rem", borderLeft: "4px solid var(--accent)" }}>
          <h3 style={{ margin: "0 0 0.5rem 0" }}>Pay Remaining Dues</h3>
          <p style={{ margin: "0 0 1rem 0" }}>Remaining Balance: Rs. {pendingAmount}</p>
          <div className="qr-box" style={{ textAlign: "center", margin: "1rem 0" }}>
            <p style={{ marginBottom: "0.5rem", fontWeight: "bold" }}>Scan to pay</p>
            <img src={`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa=somarwal@upi&pn=SomarwalInstitute`} alt="UPI QR Code" style={{ display: "inline-block" }} />
          </div>
          <input type="number" min="1" max={pendingAmount} name="paid_amount" placeholder="Amount Paid" value={payForm.paid_amount} onChange={(e) => setPayForm({...payForm, paid_amount: e.target.value})} required />
          <input type="text" name="transaction_id" placeholder="UPI Transaction ID (Required)" value={payForm.transaction_id} onChange={(e) => setPayForm({...payForm, transaction_id: e.target.value})} required />
          <div style={{ display: "flex", gap: "1rem" }}>
            <button className="primary" type="submit"><Send size={18} /> Submit Details</button>
            <button className="secondary" type="button" onClick={() => setShowPay(false)}>Cancel</button>
          </div>
        </form>
      )}

      <div className="dashboard-grid">
        <Table title="Fees" rows={data.fees} cols={["receipt_no", "paid_amount", "pending_amount", "payment_mode", "transaction_id", "status"]} />
        <Table title="Results" rows={data.results} cols={["exam_name", "marks", "percentage", "grade"]} />
        <Table title="Study Material" rows={data.materials} cols={["title", "type", "file_url"]} />
      </div>
    </section>
  );
}

function Table({ title, rows = [], cols = [] }) {
  return (
    <div className="table-panel">
      <h2>{title}</h2>
      <div className="table-scroll">
        <table>
          <thead><tr>{cols.map((col) => <th key={col}>{col.replaceAll("_", " ")}</th>)}</tr></thead>
          <tbody>{rows.map((row, index) => <tr key={row.id || index}>{cols.map((col) => <td key={col}>{React.isValidElement(row[col]) ? row[col] : String(row[col] ?? "-")}</td>)}</tr>)}</tbody>
        </table>
      </div>
    </div>
  );
}

function Footer() {
  return (
    <footer>
      <div><strong>Somarwal Computer & Tech Institute</strong><span>Ajmer, Rajasthan</span></div>
      <div className="footer-actions"><span><Phone size={16} /> +91 98282 72202</span><span><Mail size={16} /> info@somarwal.edu</span><span><MapPin size={16} /> Ajmer</span><span><Sparkles size={16} /> Admissions Open 2026</span></div>
    </footer>
  );
}

createRoot(document.getElementById("root")).render(<App />);
