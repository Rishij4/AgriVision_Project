import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000/api";

/* =========================================================
   UI TRANSLATIONS
========================================================= */

const translations = {
  english: {
    login: "Login",
    register: "Create Account",
    createAccount: "Create a new account",
    backToLogin: "Back to login",
    username: "Username",
    password: "Password",

    appSubtitle:
      "AI-assisted crop health analysis",

    dashboardSubtitle:
      "AI Crop Health Analysis",

    greeting: "Hi",
    logout: "Logout",

    heroTitle:
      "Crop Disease Detection",

    heroText:
      "Upload a clear crop or leaf image for AI-assisted health analysis.",

    newAnalysis:
      "New Analysis",

    supportedFormats:
      "Supported formats: JPG, PNG and WEBP. Maximum size: 10 MB.",

    analyze:
      "Analyze Image",

    analyzing:
      "Analyzing...",

    clear:
      "Clear",

    aiResult:
      "AI Result",

    uploadInstruction:
      "Upload an image and click Analyze Image to see the result.",

    confidence:
      "Confidence",

    severity:
      "Severity",

    imageQuality:
      "Image Quality",

    symptoms:
      "Symptoms",

    recommendations:
      "Recommended Actions",

    notes:
      "Notes",

    history:
      "Analysis History",

    historySubtitle:
      "Previous crop health analyses",

    noHistory:
      "No analysis history yet.",

    totalAnalyses:
      "Total Analyses",

    averageConfidence:
      "Average Confidence",

    lastAnalysis:
      "Last Analysis",

    noAnalyses:
      "No analyses",

    pdf:
      "PDF",

    footer:
      "AgriVision • AI-assisted crop health screening",

    selectLanguage:
      "Language",

    translation:
      "Loading...",

    connectionError:
      "Cannot connect to backend.",

    analysisFailed:
      "Analysis failed.",

    chooseImage:
      "Please choose an image first.",

    pleaseWait:
      "Please wait...",
  },

  hindi: {
    login: "लॉगिन",
    register: "खाता बनाएं",
    createAccount: "नया खाता बनाएं",
    backToLogin: "लॉगिन पर वापस जाएं",
    username: "उपयोगकर्ता नाम",
    password: "पासवर्ड",

    appSubtitle:
      "AI आधारित फसल स्वास्थ्य विश्लेषण",

    dashboardSubtitle:
      "AI फसल स्वास्थ्य विश्लेषण",

    greeting: "नमस्ते",
    logout: "लॉगआउट",

    heroTitle:
      "फसल रोग पहचान",

    heroText:
      "AI आधारित स्वास्थ्य विश्लेषण के लिए फसल या पत्ते की स्पष्ट तस्वीर अपलोड करें।",

    newAnalysis:
      "नया विश्लेषण",

    supportedFormats:
      "समर्थित प्रारूप: JPG, PNG और WEBP। अधिकतम आकार: 10 MB।",

    analyze:
      "तस्वीर का विश्लेषण करें",

    analyzing:
      "विश्लेषण हो रहा है...",

    clear:
      "साफ़ करें",

    aiResult:
      "AI परिणाम",

    uploadInstruction:
      "तस्वीर अपलोड करें और परिणाम देखने के लिए विश्लेषण करें पर क्लिक करें।",

    confidence:
      "विश्वसनीयता",

    severity:
      "गंभीरता",

    imageQuality:
      "तस्वीर की गुणवत्ता",

    symptoms:
      "लक्षण",

    recommendations:
      "सुझाए गए उपाय",

    notes:
      "टिप्पणियां",

    history:
      "विश्लेषण इतिहास",

    historySubtitle:
      "पिछले फसल स्वास्थ्य विश्लेषण",

    noHistory:
      "अभी तक कोई विश्लेषण नहीं है।",

    totalAnalyses:
      "कुल विश्लेषण",

    averageConfidence:
      "औसत विश्वसनीयता",

    lastAnalysis:
      "अंतिम विश्लेषण",

    noAnalyses:
      "कोई विश्लेषण नहीं",

    pdf:
      "PDF",

    footer:
      "AgriVision • AI आधारित फसल स्वास्थ्य जांच",

    selectLanguage:
      "भाषा",

    translation:
      "लोड हो रहा है...",

    connectionError:
      "बैकएंड से कनेक्ट नहीं हो सका।",

    analysisFailed:
      "विश्लेषण विफल हुआ।",

    chooseImage:
      "कृपया पहले एक तस्वीर चुनें।",

    pleaseWait:
      "कृपया प्रतीक्षा करें...",
  },

  telugu: {
    login: "లాగిన్",
    register: "ఖాతాను సృష్టించండి",
    createAccount: "కొత్త ఖాతాను సృష్టించండి",
    backToLogin: "లాగిన్‌కు తిరిగి వెళ్లండి",
    username: "వినియోగదారు పేరు",
    password: "పాస్‌వర్డ్",

    appSubtitle:
      "AI ఆధారిత పంట ఆరోగ్య విశ్లేషణ",

    dashboardSubtitle:
      "AI పంట ఆరోగ్య విశ్లేషణ",

    greeting: "నమస్కారం",
    logout: "లాగ్ అవుట్",

    heroTitle:
      "పంట వ్యాధి గుర్తింపు",

    heroText:
      "AI ఆధారిత ఆరోగ్య విశ్లేషణ కోసం పంట లేదా ఆకుకు సంబంధించిన స్పష్టమైన చిత్రాన్ని అప్‌లోడ్ చేయండి.",

    newAnalysis:
      "కొత్త విశ్లేషణ",

    supportedFormats:
      "మద్దతు ఉన్న ఫార్మాట్లు: JPG, PNG మరియు WEBP. గరిష్ట పరిమాణం: 10 MB.",

    analyze:
      "చిత్రాన్ని విశ్లేషించండి",

    analyzing:
      "విశ్లేషిస్తోంది...",

    clear:
      "తొలగించండి",

    aiResult:
      "AI ఫలితం",

    uploadInstruction:
      "చిత్రాన్ని అప్‌లోడ్ చేసి ఫలితాన్ని చూడటానికి విశ్లేషించండి పై క్లిక్ చేయండి.",

    confidence:
      "నమ్మక స్థాయి",

    severity:
      "తీవ్రత",

    imageQuality:
      "చిత్ర నాణ్యత",

    symptoms:
      "లక్షణాలు",

    recommendations:
      "సిఫార్సు చేసిన చర్యలు",

    notes:
      "గమనికలు",

    history:
      "విశ్లేషణ చరిత్ర",

    historySubtitle:
      "మునుపటి పంట ఆరోగ్య విశ్లేషణలు",

    noHistory:
      "ఇంకా విశ్లేషణ చరిత్ర లేదు.",

    totalAnalyses:
      "మొత్తం విశ్లేషణలు",

    averageConfidence:
      "సగటు నమ్మక స్థాయి",

    lastAnalysis:
      "చివరి విశ్లేషణ",

    noAnalyses:
      "విశ్లేషణలు లేవు",

    pdf:
      "PDF",

    footer:
      "AgriVision • AI ఆధారిత పంట ఆరోగ్య పరీక్ష",

    selectLanguage:
      "భాష",

    translation:
      "లోడ్ అవుతోంది...",

    connectionError:
      "బ్యాకెండ్‌కు కనెక్ట్ కాలేదు.",

    analysisFailed:
      "విశ్లేషణ విఫలమైంది.",

    chooseImage:
      "దయచేసి ముందుగా చిత్రాన్ని ఎంచుకోండి.",

    pleaseWait:
      "దయచేసి వేచి ఉండండి...",
  },
};


/* =========================================================
   APP
========================================================= */

function App() {

  /* =======================================================
     SESSION
  ======================================================= */

  const [token, setToken] = useState(
    sessionStorage.getItem("token") || ""
  );

  const [username, setUsername] = useState(
    sessionStorage.getItem("username") || ""
  );


  /* =======================================================
     LANGUAGE
  ======================================================= */

  const [language, setLanguage] = useState(
    sessionStorage.getItem("language") ||
      "english"
  );

  const t =
    translations[language] ||
    translations.english;


  /* =======================================================
     AUTH
  ======================================================= */

  const [mode, setMode] =
    useState("login");

  const [form, setForm] = useState({
    username: "",
    password: "",
  });


  /* =======================================================
     ANALYSIS
  ======================================================= */

  const [file, setFile] =
    useState(null);

  const [preview, setPreview] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [history, setHistory] =
    useState([]);

  const [message, setMessage] =
    useState("");

  const [busy, setBusy] =
    useState(false);

  const [changingLanguage, setChangingLanguage] =
    useState(false);


  /* =======================================================
     LOGOUT
  ======================================================= */

  function logout() {

    sessionStorage.removeItem("token");
    sessionStorage.removeItem("username");

    setToken("");
    setUsername("");

    setResult(null);
    setHistory([]);

    setFile(null);
    setPreview("");

    setMessage("");
  }


  /* =======================================================
     AUTH
  ======================================================= */

  async function auth(e) {

    e.preventDefault();

    setMessage("");
    setBusy(true);

    try {

      const response =
        await fetch(
          `${API}/auth/${mode}`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify(form),
          }
        );

      const data =
        await response.json();

      if (!response.ok) {

        setMessage(
          data.detail ||
            "Authentication failed"
        );

        return;
      }


      /* REGISTER */

      if (mode === "register") {

        setMessage(
          language === "english"
            ? "Registration successful. You can now login."
            : language === "hindi"
            ? "पंजीकरण सफल हुआ। अब आप लॉगिन कर सकते हैं।"
            : "రిజిస్ట్రేషన్ విజయవంతమైంది. ఇప్పుడు మీరు లాగిన్ చేయవచ్చు."
        );

        setMode("login");

        setForm({
          username:
            form.username,

          password:
            "",
        });

        return;
      }


      /* LOGIN */

      sessionStorage.setItem(
        "token",
        data.token
      );

      sessionStorage.setItem(
        "username",
        data.username
      );

      setToken(data.token);
      setUsername(data.username);

      setForm({
        username: "",
        password: "",
      });

    } catch (error) {

      console.error(
        "Authentication error:",
        error
      );

      setMessage(
        t.connectionError
      );

    } finally {

      setBusy(false);
    }
  }


  /* =======================================================
     LOAD HISTORY
     
     IMPORTANT:
     This ONLY reads MongoDB.
     It does NOT call Gemini.
  ======================================================= */

  async function loadHistory(
    selectedLanguage = language
  ) {

    if (!token) {
      return [];
    }

    try {

      const response =
        await fetch(
          `${API}/analysis/history?language=${encodeURIComponent(
            selectedLanguage
          )}`,
          {
            headers: {
              Authorization:
                `Bearer ${token}`,
            },
          }
        );


      if (
        response.status ===
        401
      ) {

        logout();

        return [];
      }


      const data =
        await response.json();


      if (!response.ok) {

        console.error(
          "History error:",
          data
        );

        return [];
      }


      setHistory(
        data
      );

      return data;

    } catch (error) {

      console.error(
        "History connection error:",
        error
      );

      return [];
    }
  }


  /* =======================================================
     CHANGE LANGUAGE
     
     IMPORTANT:
     
     NO GEMINI CALL.
     
     We retrieve the selected language
     directly from MongoDB.
  ======================================================= */

  async function changeLanguage(
    newLanguage
  ) {

    if (
      !newLanguage ||
      newLanguage === language
    ) {
      return;
    }


    /* Change page UI immediately */

    setLanguage(
      newLanguage
    );

    sessionStorage.setItem(
      "language",
      newLanguage
    );

    setMessage("");


    /*
      If not logged in, only UI needs
      to change.
    */

    if (!token) {
      return;
    }


    setChangingLanguage(
      true
    );


    try {

      /*
        Retrieve ALL history in selected
        language from MongoDB.

        No Gemini call.
      */

      const translatedHistory =
        await loadHistory(
          newLanguage
        );


      /*
        Keep current AI result visible.

        Find the same analysis by ID
        in the newly returned history.
      */

      if (result?.id) {

        const currentAnalysis =
          translatedHistory.find(
            item =>
              item.id ===
              result.id
          );


        if (currentAnalysis) {

          setResult(
            currentAnalysis
          );
        }
      }

    } catch (error) {

      console.error(
        "Language change error:",
        error
      );

      setMessage(
        translations[
          newLanguage
        ].connectionError
      );

    } finally {

      setChangingLanguage(
        false
      );
    }
  }


  /* =======================================================
     FILE SELECTION
  ======================================================= */

  function handleFileChange(
    e
  ) {

    const selectedFile =
      e.target.files[0];

    if (!selectedFile) {

      setFile(null);
      setPreview("");

      return;
    }

    setFile(
      selectedFile
    );

    setPreview(
      URL.createObjectURL(
        selectedFile
      )
    );

    setMessage("");
  }


  /* =======================================================
     CLEAR
  ======================================================= */

  function clearAnalysis() {

    setFile(null);
    setPreview("");
    setResult(null);
    setMessage("");
  }


  /* =======================================================
     LOAD HISTORY AFTER LOGIN
  ======================================================= */

  useEffect(() => {

    if (token) {

      loadHistory(
        language
      );
    }

  }, [token]);


  /* =======================================================
     ANALYZE IMAGE
  ======================================================= */

  async function analyze() {

    if (!file) {

      setMessage(
        t.chooseImage
      );

      return;
    }


    setBusy(true);
    setMessage("");
    setResult(null);


    const formData =
      new FormData();

    formData.append(
      "file",
      file
    );


    try {

      /*
        Backend sends the image to Gemini
        ONCE.

        Gemini returns:
        English + Hindi + Telugu.

        Backend saves all three in MongoDB.
      */

      const response =
        await fetch(
          `${API}/analysis/analyze?language=${encodeURIComponent(
            language
          )}`,
          {
            method: "POST",

            headers: {
              Authorization:
                `Bearer ${token}`,
            },

            body: formData,
          }
        );


      const data =
        await response.json();


      if (
        response.status ===
        401
      ) {

        logout();
        return;
      }


      if (!response.ok) {

        setMessage(
          data.detail ||
            t.analysisFailed
        );

        return;
      }


      /*
        Backend returns the selected
        language version.
      */

      setResult(
        data
      );


      /*
        Reload history in selected language.

        This reads MongoDB only.
      */

      await loadHistory(
        language
      );

    } catch (error) {

      console.error(
        "Analysis error:",
        error
      );

      setMessage(
        t.connectionError
      );

    } finally {

      setBusy(false);
    }
  }


  /* =======================================================
     DOWNLOAD PDF
  ======================================================= */

 async function downloadPDF(
  analysisId
) {

  setMessage("");

  try {

    const response =
      await fetch(
        `${API}/reports/${analysisId}/pdf?language=${encodeURIComponent(language)}`,
        {
          method: "GET",

          headers: {
            Authorization:
              `Bearer ${token}`,
          },
        }
      );


    if (
      response.status ===
      401
    ) {

      logout();
      return;
    }


    if (!response.ok) {

      const data =
        await response
          .json()
          .catch(
            () => null
          );

      setMessage(
        data?.detail ||
          "Failed to generate PDF."
      );

      return;
    }


    const blob =
      await response.blob();


    const url =
      window.URL.createObjectURL(
        blob
      );


    const link =
      document.createElement(
        "a"
      );


    link.href =
      url;


    link.download =
      `agrivision-${analysisId}-${language}.pdf`;


    document.body.appendChild(
      link
    );


    link.click();


    link.remove();


    window.URL.revokeObjectURL(
      url
    );

  } catch (error) {

    console.error(
      "PDF error:",
      error
    );

    setMessage(
      "Failed to download PDF."
    );
  }
}


  /* =======================================================
     SUMMARY
  ======================================================= */

  const totalAnalyses =
    history.length;


  const averageConfidence =
    history.length > 0
      ? Math.round(
          history.reduce(
            (
              sum,
              item
            ) =>
              sum +
              Number(
                item.confidence_percent ||
                  0
              ),
            0
          ) /
            history.length
        )
      : 0;


  const lastAnalysis =
    history.length > 0 &&
    history[0].created_at
      ? new Date(
          history[0].created_at
        ).toLocaleDateString()
      : t.noAnalyses;


  /* =======================================================
     LOGIN PAGE
  ======================================================= */

  if (!token) {

    return (
      <div className="auth">

        <div className="card auth-card">

          {/* LANGUAGE */}

          <div className="auth-language">

            <label>
              🌐
            </label>

            <select
              className="language-select"

              value={
                language
              }

              onChange={
                e =>
                  changeLanguage(
                    e.target.value
                  )
              }
            >

              <option value="english">
                English
              </option>

              <option value="hindi">
                हिंदी
              </option>

              <option value="telugu">
                తెలుగు
              </option>

            </select>

          </div>


          <div className="logo">
            🌱
          </div>


          <h1>
            🌱 AgriVision
          </h1>


          <p className="subtitle">
            {t.appSubtitle}
          </p>


          {/* AUTH FORM */}

          <form
            onSubmit={
              auth
            }
          >

            <input
              type="text"

              placeholder={
                t.username
              }

              value={
                form.username
              }

              onChange={
                e =>
                  setForm({
                    ...form,

                    username:
                      e.target.value,
                  })
              }

              required
            />


            <input
              type="password"

              placeholder={
                t.password
              }

              value={
                form.password
              }

              onChange={
                e =>
                  setForm({
                    ...form,

                    password:
                      e.target.value,
                  })
              }

              required
            />


            <button
              type="submit"
              disabled={busy}
            >

              {busy
                ? t.pleaseWait
                : mode === "login"
                ? t.login
                : t.register}

            </button>

          </form>


          {message && (
            <p className="message">
              {message}
            </p>
          )}


          <button
            className="link-button"

            onClick={() => {

              setMode(
                mode === "login"
                  ? "register"
                  : "login"
              );

              setMessage("");

            }}
          >

            {mode === "login"
              ? t.createAccount
              : t.backToLogin}

          </button>

        </div>

      </div>
    );
  }


  /* =======================================================
     MAIN APPLICATION
  ======================================================= */

  return (
    <div className="app">


      {/* =================================================
          HEADER
      ================================================= */}

      <header className="header">

        <div>

          <h1>
            🌱 AgriVision
          </h1>

          <p>
            {t.dashboardSubtitle}
          </p>

        </div>


        <div className="user-area">

          {/* LANGUAGE */}

          <div className="language-wrapper">

            <span>
              🌐
            </span>

            <select
              className="language-select"

              value={
                language
              }

              disabled={
                changingLanguage
              }

              onChange={
                e =>
                  changeLanguage(
                    e.target.value
                  )
              }
            >

              <option value="english">
                🇬🇧 English
              </option>

              <option value="hindi">
                🇮🇳 हिंदी
              </option>

              <option value="telugu">
                🇮🇳 తెలుగు
              </option>

            </select>

          </div>


          {changingLanguage && (
            <span className="translation-status">
              🌐 {t.translation}
            </span>
          )}


          {/* USER */}

          <span>
            {t.greeting},{" "}
            <b>
              {username}
            </b>
          </span>


          {/* LOGOUT */}

          <button
            className="logout"

            onClick={
              logout
            }
          >
            {t.logout}
          </button>

        </div>

      </header>


      {/* =================================================
          HERO
      ================================================= */}

      <section className="hero">

        <h2>
          {t.heroTitle}
        </h2>

        <p>
          {t.heroText}
        </p>

      </section>


      {/* =================================================
          SUMMARY
      ================================================= */}

      <div className="summary-grid">

        <div className="summary-card">

          <div className="summary-icon">
            📊
          </div>

          <div>

            <span>
              {t.totalAnalyses}
            </span>

            <strong>
              {totalAnalyses}
            </strong>

          </div>

        </div>


        <div className="summary-card">

          <div className="summary-icon">
            🎯
          </div>

          <div>

            <span>
              {t.averageConfidence}
            </span>

            <strong>
              {averageConfidence}%
            </strong>

          </div>

        </div>


        <div className="summary-card">

          <div className="summary-icon">
            🕒
          </div>

          <div>

            <span>
              {t.lastAnalysis}
            </span>

            <strong>
              {lastAnalysis}
            </strong>

          </div>

        </div>

      </div>


      {/* =================================================
          MAIN GRID
      ================================================= */}

      <div className="grid">


        {/* =================================================
            NEW ANALYSIS
        ================================================= */}

        <div className="card">

          <div className="upload-header">

            <h2>
              📷 {t.newAnalysis}
            </h2>


            {(file || result) && (

              <button
                className="clear-button"

                onClick={
                  clearAnalysis
                }
              >
                ✕ {t.clear}
              </button>

            )}

          </div>


          <p className="description">
            {t.supportedFormats}
          </p>


          <input
            type="file"

            accept="
              image/jpeg,
              image/png,
              image/webp
            "

            onChange={
              handleFileChange
            }
          />


          {/* PREVIEW */}

          {preview && (

            <div className="preview-container">

              <img
                src={preview}

                alt="Selected crop"

                className="preview"
              />

            </div>

          )}


          <button
            onClick={
              analyze
            }

            disabled={
              busy ||
              !file ||
              changingLanguage
            }
          >

            {busy
              ? `🤖 ${t.analyzing}`
              : `🔍 ${t.analyze}`}

          </button>


          {message && (
            <p className="error">
              {message}
            </p>
          )}

        </div>


        {/* =================================================
            AI RESULT
        ================================================= */}

        <div className="card">

          <div className="result-header">

            <h2>
              🤖 {t.aiResult}
            </h2>


            {result && (

              <button
                className="small-button"

                onClick={() =>
                  downloadPDF(
                    result.id
                  )
                }

                disabled={
                  changingLanguage
                }
              >
                📄 {t.pdf}
              </button>

            )}

          </div>


          {!result ? (

            <div className="empty">

              <div className="empty-icon">
                🌿
              </div>

              <p>
                {t.uploadInstruction}
              </p>

            </div>

          ) : (

            <div className="result">

              <h3>
                {result.crop}
              </h3>


              <div className="issue">
                {result.probable_issue}
              </div>


              {/* STATS */}

              <div className="stats">

                <div className="stat">

                  <span>
                    {t.confidence}
                  </span>

                  <strong>
                    {
                      result.confidence_percent
                    }%
                  </strong>

                </div>


                <div className="stat">

                  <span>
                    {t.severity}
                  </span>

                  <strong>
                    {
                      result.severity ||
                      "N/A"
                    }
                  </strong>

                </div>


                <div className="stat">

                  <span>
                    {t.imageQuality}
                  </span>

                  <strong>
                    {
                      result.image_quality ||
                      "N/A"
                    }
                  </strong>

                </div>

              </div>


              {/* SYMPTOMS */}

              <h4>
                {t.symptoms}
              </h4>

              <ul>

                {(
                  result.symptoms ||
                  []
                ).map(
                  (
                    item,
                    index
                  ) => (

                    <li
                      key={
                        index
                      }
                    >
                      {item}
                    </li>

                  )
                )}

              </ul>


              {/* RECOMMENDATIONS */}

              <h4>
                {t.recommendations}
              </h4>

              <ul>

                {(
                  result.recommendations ||
                  []
                ).map(
                  (
                    item,
                    index
                  ) => (

                    <li
                      key={
                        index
                      }
                    >
                      {item}
                    </li>

                  )
                )}

              </ul>


              {/* NOTES */}

              {result.notes && (

                <>

                  <h4>
                    {t.notes}
                  </h4>

                  <p className="notes">
                    {result.notes}
                  </p>

                </>

              )}

            </div>
          )}

        </div>

      </div>


      {/* =================================================
          HISTORY
      ================================================= */}

      <div className="card history-card">

        <div className="history-header">

          <div>

            <h2>
              📜 {t.history}
            </h2>

            <p>
              {t.historySubtitle}
            </p>

          </div>

        </div>


        {history.length === 0 ? (

          <div className="empty-history">

            <p>
              {t.noHistory}
            </p>

          </div>

        ) : (

          <div className="history-list">

            {history.map(
              item => (

                <div
                  className="history-item"
                  key={
                    item.id
                  }
                >

                  <div className="history-info">

                    <h3>
                      {
                        item.crop ||
                        "Unknown Crop"
                      }
                    </h3>

                    <p>
                      {
                        item.probable_issue ||
                        "No issue detected"
                      }
                    </p>

                    <small>

                      {item.created_at
                        ? new Date(
                            item.created_at
                          ).toLocaleString()
                        : ""}

                    </small>

                  </div>


                  <div className="history-actions">

                    <span className="confidence">

                      {
                        item.confidence_percent ??
                        "N/A"
                      }%

                    </span>


                    <button
                      className="pdf-button"

                      onClick={() =>
                        downloadPDF(
                          item.id
                        )
                      }

                      disabled={
                        changingLanguage
                      }
                    >

                      📄 {t.pdf}

                    </button>

                  </div>

                </div>

              )
            )}

          </div>

        )}

      </div>


      {/* =================================================
          FOOTER
      ================================================= */}

      <footer>
        {t.footer}
      </footer>

    </div>
  );
}


/* =========================================================
   RENDER
========================================================= */

createRoot(
  document.getElementById("root")
).render(
  <App />
);
