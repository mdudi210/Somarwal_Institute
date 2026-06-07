const rawApiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const API_URL = rawApiUrl.endsWith("/") ? rawApiUrl.slice(0, -1) : rawApiUrl;

export function setSession(session) {
  localStorage.setItem("somarwal_user", JSON.stringify({ name: session.name, role: session.role }));
}

export function clearSession() {
  localStorage.removeItem("somarwal_user");
}

export function getStoredUser() {
  try {
    return JSON.parse(localStorage.getItem("somarwal_user") || "null");
  } catch {
    return null;
  }
}

function getCsrfToken() {
  const match = document.cookie.match(new RegExp('(^| )somarwal_csrf_token=([^;]+)'));
  return match ? match[2] : null;
}

export async function api(path, options = {}, isRetry = false) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  
  const csrfToken = getCsrfToken();
  if (csrfToken) {
    headers["X-CSRF-Token"] = csrfToken;
  }

  const fetchOptions = { ...options, headers, credentials: "include" };
  const response = await fetch(`${API_URL}${path}`, fetchOptions);
  
  // Auto-refresh logic
  if (response.status === 401 && !isRetry && path !== "/api/auth/refresh" && path !== "/api/auth/login") {
    try {
      const refreshRes = await fetch(`${API_URL}/api/auth/refresh`, {
        method: "POST",
        credentials: "include"
      });
      if (refreshRes.ok) {
        // Refresh succeeded, retry original request
        return api(path, options, true);
      } else {
        // Refresh failed (token expired/invalid), logout
        clearSession();
        window.location.hash = "/";
        window.location.reload();
        throw new Error("Session expired. Please log in again.");
      }
    } catch (e) {
      clearSession();
      window.location.hash = "/";
      window.location.reload();
      throw e;
    }
  }
  
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || data.message || "Request failed");
  return data;
}

export const fallbackHome = {
  stats: { students_trained: 1850, active_courses: 4, placements: 240, certificates: 1250 },
  courses: [
    {
      id: 1,
      name: "Diploma in Computer Applications",
      code: "DCA",
      category: "Diploma Course",
      duration: "6 Months",
      fees: 12000,
      description: "Computer foundation, office automation, internet, typing, AI basics, and employability skills.",
      syllabus: ["Computer fundamentals", "MS Word", "MS Excel", "PowerPoint", "Typing practice", "AI tools"],
      software_covered: ["Windows", "MS Office", "Canva"],
      career_options: ["Computer operator", "Office assistant", "Data entry executive"]
    },
    {
      id: 2,
      name: "Tally Prime with GST",
      code: "TALLY-GST",
      category: "Accounting",
      duration: "3 Months",
      fees: 8500,
      description: "Practical accounting, ledgers, vouchers, GST returns, inventory, and reports.",
      syllabus: ["Accounting basics", "Vouchers", "GST", "Inventory", "Reports"],
      software_covered: ["Tally Prime", "Excel"],
      career_options: ["Account assistant", "Billing executive"]
    }
  ],
  gallery: [
    { id: 1, title: "Modern Computer Lab", category: "Labs", image: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80" },
    { id: 2, title: "Practical Training", category: "Events", image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80" }
  ],
  reviews: [
    { id: 1, student_name: "Neha Soni", course: "DCA", rating: 5, message: "The classes were simple, disciplined, and focused on real computer practice." },
    { id: 2, student_name: "Aman Khan", course: "Tally Prime", rating: 5, message: "Practical GST entries and reports helped me get billing work quickly." }
  ],
  placements: [
    { id: 1, student_name: "Rahul Meena", company: "Ajmer Digital Services", package: "2.4 LPA", course: "DCA" }
  ]
};
