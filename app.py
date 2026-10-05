import streamlit as st
import streamlit.components.v1 as components
import requests
import random
import time

# ==========================================
# CẤU HÌNH API
# ==========================================
API_URL = "https://script.google.com/macros/s/AKfycbzAXrdKJbHeus5XfIS3F9hf_USz3aC87sCx2jNM7gTDoWLmXkokE6T8m0BzeSWfdh55XA/exec" # Dán link Google Apps Script vào đây

st.set_page_config(page_title="Hệ Thống Kiểm Tra", layout="wide", page_icon="💻")

# ==========================================
# 1. BẢO VỆ TOÁN HỌC & CHỐNG GIAN LẬN XUYÊN KHUNG
# ==========================================
global_js = """
<script>
    const pWin = window.parent || window;
    const pDoc = pWin.document;

    // --- BẢO VỆ CÔNG THỨC TOÁN ---
    if (!pDoc.querySelector('meta[name="google"]')) {
        let meta = pDoc.createElement('meta');
        meta.name = 'google';
        meta.content = 'notranslate';
        pDoc.head.appendChild(meta);
    }
    pDoc.documentElement.lang = 'vi';
    pDoc.documentElement.setAttribute('translate', 'no');
    pDoc.body.classList.add('notranslate');

    // --- ÉP CỘT ĐỒNG HỒ TRƯỢT THEO (STICKY) ---
    function makeSticky() {
        let containers = pDoc.querySelectorAll('.stMain > div, .block-container');
        containers.forEach(c => {
            c.style.overflow = 'visible';
            c.style.clipPath = 'none';
        });

        let cols = pDoc.querySelectorAll('[data-testid="column"]');
        if(cols.length > 0) {
            cols[0].style.position = '-webkit-sticky';
            cols[0].style.position = 'sticky';
            cols[0].style.top = '25px';
            cols[0].style.alignSelf = 'flex-start';
            cols[0].style.zIndex = '9999';
        }
    }
    setInterval(makeSticky, 500);

    // --- ẨN NÚT "GianLan" HOÀN TOÀN BẰNG JAVASCRIPT ---
    setInterval(() => {
        let btns = pDoc.querySelectorAll('button');
        btns.forEach(b => {
            if (b.innerText === 'GianLan') {
                b.style.display = 'none'; 
                let wrapper = b.closest('div[data-testid="stElementContainer"]');
                if (wrapper) {
                    wrapper.style.display = 'none'; 
                    wrapper.style.height = '0px';
                }
            }
        });
    }, 100);

    // --- HỆ THỐNG CHỐNG GIAN LẬN BẮT GỬI TÍN HIỆU VỀ PYTHON ---
    if (!pWin.antiCheatTracker_v3) {
        pWin.antiCheatTracker_v3 = true;
        pWin.lastCheatTime = 0;
        
        function triggerPythonCheat() {
            let now = Date.now();
            if (now - pWin.lastCheatTime < 2000) return; 
            
            let bodyText = pDoc.body.innerText || "";
            if (!bodyText.includes("THỜI GIAN CÒN LẠI")) return;

            let btns = pDoc.querySelectorAll('button');
            btns.forEach(b => {
                if (b.innerText === 'GianLan') {
                    pWin.lastCheatTime = now;
                    b.click(); // Âm thầm tự động click gửi về máy chủ
                }
            });
        }

        pDoc.addEventListener("visibilitychange", () => {
            if (pDoc.hidden || pDoc.visibilityState === 'hidden') {
                triggerPythonCheat();
            }
        });
        
        pWin.addEventListener("blur", () => {
            triggerPythonCheat();
        });

        pDoc.addEventListener('contextmenu', event => event.preventDefault());
        
        pDoc.addEventListener('keydown', function(e) {
            if(e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I') || (e.ctrlKey && ['c', 'v', 'p'].includes(e.key.toLowerCase()))) {
                e.preventDefault();
            }
        });
    }
</script>
"""
components.html(global_js, height=0, width=0)

# ==========================================
# 2. CSS THEME HACKER / CYBERPUNK
# ==========================================
cyber_css = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 1rem !important; 
        margin-top: -30px !important;
    }

    /* THANH TRƯỢT DỌC KHỔNG LỒ (CYAN) */
    [data-testid="stAppViewContainer"], .stApp { overflow-y: auto !important; }
    ::-webkit-scrollbar, *::-webkit-scrollbar, [data-testid="stAppViewContainer"]::-webkit-scrollbar {
        width: 18px !important; background-color: #050505 !important; display: block !important;
    }
    ::-webkit-scrollbar-track, *::-webkit-scrollbar-track {
        background-color: #050505 !important; border-left: 1px solid #00f3ff !important;
    }
    ::-webkit-scrollbar-thumb, *::-webkit-scrollbar-thumb {
        background-color: #00f3ff !important; border-radius: 0px !important; border: 2px solid #050505 !important; 
    }
    ::-webkit-scrollbar-thumb:hover, *::-webkit-scrollbar-thumb:hover { background-color: #00b3bd !important; }

    /* CƯỠNG CHẾ GIAO DIỆN DARK MODE */
    :root, body, html { color-scheme: dark !important; background-color: #050505 !important; }
    [data-testid="stAppViewContainer"], .stApp {
        background-color: #050505 !important;
        background-image: linear-gradient(rgba(0, 243, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 243, 255, 0.05) 1px, transparent 1px) !important;
        background-size: 40px 40px !important;
        color: #e2e8f0 !important;
    }
    html, body, p, span, label, div, h1, h2, h3, h4 { 
        font-family: 'Segoe UI', monospace, sans-serif !important;
        color: #e2e8f0 !important; 
    }

    /* THANH TOP BAR */
    .cyber-top-bar {
        background-color: #000000; border-bottom: 2px solid #00f3ff;
        padding: 15px 25px; margin-top: -50px; margin-bottom: 30px;
        display: flex; align-items: center; box-shadow: 0 4px 15px rgba(0, 243, 255, 0.1);
    }
    .cyber-top-arrow { color: #00f3ff; font-weight: 900; font-size: 1.4rem; margin-right: 15px; }
    .cyber-top-text { color: #ffffff; font-weight: bold; font-size: 1.2rem; letter-spacing: 2px; }

    /* TIÊU ĐỀ LOGIN */
    .cyber-login-title {
        text-align: center; color: #ffffff; font-weight: 900; font-size: 2rem; 
        letter-spacing: 3px; text-shadow: 0 0 10px rgba(255,255,255,0.5); margin-top: 10px;
    }

    /* Ô NHẬP LIỆU */
    div[data-testid="stTextInput"] label p { color: #00f3ff !important; font-size: 1rem !important; }
    div[data-testid="stTextInput"] input {
        background-color: #050505 !important; color: #00f3ff !important;
        border: 1px solid #005f66 !important; border-radius: 0px !important;
        font-size: 1.1rem !important; padding: 12px !important;
    }

    /* CHUẨN HÓA LẠI CỠ CHỮ TOÁN HỌC (KATEX) */
    .katex, .katex-html { 
        font-size: 1.1em !important; 
        color: #00f3ff !important; 
    }

    /* NÚT BẤM BẢNG ĐIỀU HƯỚNG C1, C2 */
    div[data-testid="stVerticalBlock"]:has(span#nav-grid-marker) div[data-testid="stButton"] button {
        font-size: 1.1rem !important; padding: 5px !important; min-height: 40px !important;
    }
    div[data-testid="stVerticalBlock"]:has(span#nav-grid-marker) div[data-testid="stButton"] button[kind="primary"] {
        background: #701a75 !important; color: #ffffff !important; border: 1px solid #d946ef !important; 
        box-shadow: 0 0 10px rgba(217, 70, 239, 0.4) !important;
    }
    div[data-testid="stVerticalBlock"]:has(span#nav-grid-marker) div[data-testid="stButton"] button[kind="secondary"] {
        background: #000000 !important; color: #00f3ff !important; border: 1px solid #005f66 !important; 
    }
    div[data-testid="stVerticalBlock"]:has(span#nav-grid-marker) div[data-testid="stButton"] button:hover { border-color: #00f3ff !important; }

    /* NÚT XÁC NHẬN / NỘP BÀI */
    div[data-testid="stButton"] button[kind="primary"] {
        background: #3b0764 !important; color: #d946ef !important; 
        border: 1px solid #a21caf !important; border-radius: 0px !important; 
        padding: 10px !important; font-size: 1.1rem !important; font-weight: bold !important;
        letter-spacing: 1px !important; text-transform: uppercase !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #581c87 !important; color: #ffffff !important; box-shadow: 0 0 15px rgba(192, 38, 211, 0.6) !important;
    }
    div[data-testid="stButton"] button[kind="secondary"] {
        background: transparent !important; color: #00f3ff !important; border: 1px solid #00f3ff !important;
        border-radius: 0px !important; padding: 10px !important; width: 100% !important; font-size: 1.1rem !important;
    }

    /* KHUNG CÂU HỎI CHÍNH */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #000000 !important; border: 1px solid #00f3ff !important; 
        border-radius: 0px !important; margin-bottom: 30px !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.08) inset !important;
    }
    .q-header-box {
        background: #001a1a; color: #00f3ff !important;
        font-weight: bold; font-size: 1.2rem; padding: 10px 20px;
        border-bottom: 1px solid #00f3ff; text-transform: uppercase; letter-spacing: 1px;
    }
    h4 {
        padding: 20px 25px 10px 25px !important; font-size: 1.35rem !important;
        font-weight: normal !important; line-height: 1.6 !important; color: #ffffff !important; margin: 0 !important;
    }
    
    /* DẠNG 1: LƯỚI ĐÁP ÁN TRẮC NGHIỆM 2x2 */
    div[data-testid="stVerticalBlock"]:has(#type1-container) div[role="radiogroup"] {
        display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 15px !important;
        width: 100% !important; padding: 10px 25px 25px 25px !important;
    }
    div[data-testid="stVerticalBlock"]:has(#type1-container) div[role="radiogroup"] > label {
        background-color: #0a0a0a !important; border: 1px solid #005f66 !important; border-radius: 0px !important;
        padding: 15px !important; margin: 0 !important; display: flex !important; align-items: center !important;
        min-height: 70px !important; transition: all 0.2s ease !important;
    }
    div[data-testid="stVerticalBlock"]:has(#type1-container) div[role="radiogroup"] > label:hover {
        background-color: #001a1a !important; border-color: #00f3ff !important;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.2) inset !important;
    }
    div[data-testid="stVerticalBlock"]:has(#type1-container) div[role="radiogroup"] label p {
        font-size: 1.2rem !important; color: #ffffff !important; margin-left: 10px !important; line-height: 1.5 !important;
    }

    /* DẠNG 2: MỆNH ĐỀ ĐÚNG SAI */
    div[data-testid="stVerticalBlock"]:has(> div #table-d2) {
        border: none !important; background: transparent !important; margin: 10px 25px 20px 25px !important; padding: 0 !important;
    }
    div[data-testid="stVerticalBlock"]:has(> div #table-d2) > div[data-testid="stHorizontalBlock"] {
        border-bottom: 1px dashed #005f66 !important; padding: 10px 0 !important; align-items: center !important;
    }
    div[data-testid="stVerticalBlock"]:has(> div #table-d2) > div[data-testid="stHorizontalBlock"]:last-child { border-bottom: none !important; }
    div[data-testid="stVerticalBlock"]:has(> div #table-d2) div[data-testid="column"]:first-child {
        padding: 5px 10px !important; display: flex !important; align-items: center !important;
    }
    div[data-testid="stVerticalBlock"]:has(> div #table-d2) p {
        font-size: 1.2rem !important; line-height: 1.5 !important; margin: 0 !important; color: #ffffff !important;
    }
    div[data-testid="stVerticalBlock"]:has(> div #table-d2) div[role="radiogroup"] {
        flex-direction: row !important; justify-content: flex-end !important; gap: 20px !important; padding-right: 15px !important;
    }
    div[data-testid="stVerticalBlock"]:has(> div #table-d2) div[data-baseweb="radio"] label p {
        font-size: 1.1rem !important; color: #ffffff !important; margin-left: 5px !important;
    }

    @media (max-width: 768px) {
        div[data-testid="stVerticalBlock"]:has(#type1-container) div[role="radiogroup"] { grid-template-columns: 1fr !important; }
        .cyber-login-title { font-size: 1.5rem !important; }
        .cyber-top-text { font-size: 0.9rem !important; }
    }
</style>
"""
st.markdown(cyber_css, unsafe_allow_html=True)

# ==========================================
# 3. HEADER TOP BAR NHO NHỎ
# ==========================================
st.markdown("""
<div class='cyber-top-bar'>
    <span class='cyber-top-arrow'>&gt;_</span>
    <span class='cyber-top-text'>LỚP TOÁN THẦY LINH - 0348585044</span>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. XỬ LÝ DỮ LIỆU & ÉP KÍCH THƯỚC PHÂN SỐ
# ==========================================
def fix_latex(text):
    if not text: return ""
    text = str(text).replace(r"\frac", r"\dfrac")
    return text

@st.cache_data(ttl=60, show_spinner=False)
def fetch_data():
    try: return requests.get(API_URL).json()
    except: return None

def generate_exam(questions, config):
    d1_groups, d2_groups, d3_groups = {}, {}, {}
    for row in questions:
        dang, nhom = int(row.get('Dang', 0)), row.get('MaNhom', '')
        if dang == 1: d1_groups.setdefault(nhom, []).append(row)
        elif dang == 2: d2_groups.setdefault(nhom, []).append(row)
        elif dang == 3: d3_groups.setdefault(nhom, []).append(row)
            
    exam_questions = []
    for group in random.sample(list(d1_groups.values()), min(int(config.get("So_Cau_D1", 10)), len(d1_groups))): exam_questions.append(random.choice(group))
    for group in random.sample(list(d2_groups.values()), min(int(config.get("So_Cau_D2", 1)), len(d2_groups))): exam_questions.append(random.choice(group))
    for group in random.sample(list(d3_groups.values()), min(int(config.get("So_Cau_D3", 1)), len(d3_groups))): exam_questions.append(random.choice(group))
    return exam_questions

if 'exam_state' not in st.session_state:
    st.session_state.exam_state = 'LOGIN'
    st.session_state.questions = []
    st.session_state.config = {}
    st.session_state.start_time = 0
    st.session_state.answers = {}
    st.session_state.current_q_index = 0
    st.session_state.cheat_count = 0 

with st.spinner('Đang kết nối hệ thống máy chủ...'):
    raw_data = fetch_data()
    system_config = raw_data['config'] if raw_data and 'config' in raw_data else {}

# ==========================================
# 5. MÀN HÌNH ĐĂNG NHẬP (CYBER BOX)
# ==========================================
if st.session_state.exam_state == 'LOGIN':
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # Ô MÀU XANH PHÍA TRÊN CHỨA TÊN TRƯỜNG
        st.markdown("""
        <div style='background: #000000; border: 1px solid #00f3ff; padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(0, 243, 255, 0.08) inset; margin-bottom: 25px;'>
            <h1 style='color: #ffffff; font-size: 3.5rem; margin: 0; font-weight: 900; text-shadow: 0 0 10px rgba(255,255,255,0.5); line-height: 1.2;'>TRƯỜNG THCS VINH PHÚ 1</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # BIỂU TƯỢNG VÀ TIÊU ĐỀ
        st.markdown("<div style='text-align: center; font-size: 3rem; margin-top: 0px;'>🖧</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='cyber-login-title'>{system_config.get('Tieu_De', 'BÀI KIỂM TRA MÔN TOÁN')}</div>", unsafe_allow_html=True)
        
        # TÊN TÁC GIẢ PHÍA TRÊN PHẦN LƯU Ý
        st.markdown("<div style='text-align: center; color: #00f3ff; font-family: monospace; font-size: 1.2rem; margin-top: 15px; margin-bottom: 10px; font-weight: bold;'>TÁC GIẢ: TRẦN VĂN LINH</div>", unsafe_allow_html=True)
        
        if system_config.get("Ghi_Chu", ""): st.info(system_config.get("Ghi_Chu", ""))
        
        st.write("")
        ho_ten = st.text_input("> TÊN_HỌC_SINH", placeholder="NHẬP_DỮ_LIỆU...")
        lop = st.text_input("> MÃ_LỚP", placeholder="NHẬP_DỮ_LIỆU...")
        st.write("")
        st.write("")
        
        if st.button("XÁC THỰC ➔", type="primary", use_container_width=True):
            if ho_ten and lop:
                if raw_data and 'questions' in raw_data:
                    st.session_state.cheat_count = 0
                    st.session_state.ho_ten = ho_ten
                    st.session_state.lop = lop
                    st.session_state.config = system_config 
                    st.session_state.questions = generate_exam(raw_data['questions'], system_config)
                    st.session_state.start_time = time.time()
                    st.session_state.current_q_index = 0
                    st.session_state.exam_state = 'IN_PROGRESS'
                    st.rerun()
                else:
                    st.error("LỖI_KẾT_NỐI_MÁY_CHỦ")
            else: st.warning("> VUI_LÒNG_NHẬP_ĐẦY_ĐỦ_THÔNG_TIN")

# ==========================================
# 6. MÀN HÌNH LÀM BÀI CHÍNH
# ==========================================
elif st.session_state.exam_state == 'IN_PROGRESS':
    
    # --- HEADER LỚN TRƯỜNG THCS VINH PHÚ 1 TRONG BÀI THI ---
    st.markdown("""
    <div style="text-align: center; padding-bottom: 20px; border-bottom: 1px dashed #005f66; margin-bottom: 30px;">
        <h1 style="color: #ffffff; font-size: 3.5rem; font-weight: 900; letter-spacing: 2px; text-transform: uppercase; margin: 0; text-shadow: 0 0 15px rgba(255,255,255,0.6);">TRƯỜNG THCS VINH PHÚ 1</h1>
        <h3 style="color: #00f3ff; font-size: 1.4rem; font-family: monospace; letter-spacing: 3px; margin-top: 5px; margin-bottom: 0;">HỆ THỐNG KIỂM TRA ĐÁNH GIÁ TOÁN HỌC</h3>
    </div>
    """, unsafe_allow_html=True)

    total_q = len(st.session_state.questions)
    current_idx = st.session_state.current_q_index
    q = st.session_state.questions[current_idx]
    
    # NÚT TÀNG HÌNH NHẬN TÍN HIỆU GIAN LẬN
    if st.button("GianLan"):
        st.session_state.cheat_count += 1
        if st.session_state.cheat_count >= 3:
            st.session_state.trigger_submit = True
        st.rerun()
    
    col_nav, col_main = st.columns([1, 4.5], gap="large")
    
    # ------------------
    # CỘT TRÁI: ĐỒNG HỒ & BẢNG ĐIỀU HƯỚNG
    # ------------------
    with col_nav:
        thoi_gian_giay = int(st.session_state.config.get("Thoi_Gian_Phut", 15)) * 60
        time_left = max(0, thoi_gian_giay - (time.time() - st.session_state.start_time))
        
        components.html(f"""
        <div id="timer-box" style="background-color: #000000; border: 2px solid #00f3ff; padding: 15px 10px; text-align: center; box-shadow: 0 0 15px rgba(0, 243, 255, 0.2) inset;">
            <div id="time-title" style="color: #00f3ff; font-family: monospace; font-size: 14px; font-weight: bold; margin-bottom: 5px;">THỜI GIAN CÒN LẠI</div>
            <div id="time" style="color: #ffffff; font-size: 38px; font-family: monospace; font-weight: 900; text-shadow: 0 0 8px rgba(255,255,255,0.5);">...</div>
        </div>
        <script>
        var time_left = {int(time_left)};
        var x = setInterval(function() {{
            time_left--;
            var m = Math.floor(time_left / 60); var s = time_left % 60;
            if (s < 10) s = "0" + s;
            document.getElementById("time").innerHTML = m + ":" + s;
            
            if (time_left <= 60 && time_left > 0) {{
                document.getElementById("timer-box").style.borderColor = "#ef4444";
                document.getElementById("time").style.color = "#ef4444";
                document.getElementById("time-title").style.color = "#ef4444";
            }}
            
            if (time_left <= 0) {{ 
                clearInterval(x); 
                document.getElementById("time").innerHTML = "HẾT GIỜ";
                if(window.parent && window.parent.document) {{
                    window.parent.document.querySelectorAll('button').forEach(btn => {{
                        let text = btn.innerText || btn.textContent;
                        if(text.includes('NỘP BÀI') || text.includes('HOÀN THÀNH')) btn.click();
                    }});
                }}
            }}
        }}, 1000);
        </script>
        """, height=120)
        
        st.write("")
        st.markdown("<div style='color: #00f3ff; font-family: monospace; font-size: 14px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;'>&gt; BẢNG ĐIỀU HƯỚNG:</div>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<span id='nav-grid-marker'></span>", unsafe_allow_html=True)
            for row_idx in range(0, total_q, 2):
                cols = st.columns(2)
                for col_idx in range(2):
                    i = row_idx + col_idx
                    if i < total_q:
                        q_id = st.session_state.questions[i].get('ID', str(i))
                        dang = int(st.session_state.questions[i].get('Dang', 0))
                        ans = st.session_state.answers.get(q_id, "")
                        
                        is_answered = False
                        if dang == 1 and ans: is_answered = True
                        elif dang == 2 and ans and ("Đ" in ans or "S" in ans): is_answered = True
                        elif dang == 3 and ans.strip(): is_answered = True
                        
                        btn_type = "primary" if is_answered else "secondary"
                        
                        label = f"C{i+1}"
                        if i == current_idx: label = f"📍 {label}"
                        
                        with cols[col_idx]:
                            if st.button(label, key=f"nav_btn_{i}", type=btn_type, use_container_width=True):
                                st.session_state.current_q_index = i
                                st.rerun()

        st.write("")
        st.write("")
        submit_btn = st.button("📤 NỘP BÀI ➔", type="primary", use_container_width=True)

    # ------------------
    # CỘT PHẢI: KHUNG CÂU HỎI & ĐÁP ÁN
    # ------------------
    with col_main:
        if st.session_state.cheat_count == 1:
            st.error("🚨 **CẢNH BÁO LẦN 1:** Phát hiện chuyển Tab! Vui lòng tập trung làm bài.")
        elif st.session_state.cheat_count == 2:
            st.error("🚨 **CẢNH BÁO LẦN 2:** Cảnh báo cuối cùng! Rời màn hình lần nữa bài sẽ tự nộp.")

        st.markdown(f"<p style='color:#ffffff; font-size: 1.1rem; font-weight: bold; font-family: monospace;'>📝 BÀI THI TOÁN: {st.session_state.ho_ten.upper()} | LỚP: {st.session_state.lop.upper()}</p>", unsafe_allow_html=True)
        
        progress_pct = int(((current_idx + 1) / total_q) * 100)
        st.markdown(f"""
        <div style="width: 100%; background-color: #0a0a0a; border: 1px solid #005f66; margin-bottom: 25px; height: 8px;">
          <div style="width: {progress_pct}%; background-color: #00f3ff; height: 100%; box-shadow: 0 0 10px #00f3ff;"></div>
        </div>
        """, unsafe_allow_html=True)

        dang = int(q.get('Dang', 0))
        q_id = q.get('ID', str(current_idx))
        
        with st.container(border=True):
            st.markdown(f"<div class='q-header-box'>CÂU HỎI SỐ {current_idx + 1} / {total_q}</div>", unsafe_allow_html=True)
            
            st.markdown(f"#### {fix_latex(q.get('CauHoi', ''))}")
            st.markdown("<hr style='border-top: 1px dashed #005f66; margin-top: 10px; margin-bottom: 0;'>", unsafe_allow_html=True)
            
            if dang == 1:
                st.markdown("<div id='type1-container'></div>", unsafe_allow_html=True)
                
                options = [fix_latex(opt) for opt in [q.get('Y_A'), q.get('Y_B'), q.get('Y_C'), q.get('Y_D')] if opt]
                saved_ans = st.session_state.answers.get(q_id)
                idx = options.index(saved_ans) if saved_ans in options else None
                
                selected = st.radio(f"Lựa chọn câu {current_idx+1}:", options, key=f"ans_{q_id}", index=idx, label_visibility="collapsed")
                if selected is not None:
                    st.session_state.answers[q_id] = selected
                
            elif dang == 2:
                with st.container():
                    st.markdown("<div id='table-d2'></div>", unsafe_allow_html=True)
                    
                    saved_str = st.session_state.answers.get(q_id, "")
                    saved_parts = [s.strip() for s in saved_str.split(",")] if saved_str else []
                    ans_parts = []
                    
                    for y_idx, y_text in zip(['a', 'b', 'c', 'd'], [q.get('Y_A'), q.get('Y_B'), q.get('Y_C'), q.get('Y_D')]):
                        if str(y_text).strip():
                            saved_choice = saved_parts[['a','b','c','d'].index(y_idx)] if len(saved_parts) > ['a','b','c','d'].index(y_idx) else ""
                            r_idx = 0 if saved_choice == "Đ" else (1 if saved_choice == "S" else None)
                            
                            c1, c2 = st.columns([7, 3]) 
                            with c1: 
                                st.markdown(f"**Mệnh đề {y_idx}):** &nbsp; {fix_latex(y_text)}")
                            with c2:
                                choice = st.radio(f"Chọn {y_idx}", ["Đúng", "Sai"], key=f"ans_{q_id}_{y_idx}", horizontal=True, index=r_idx, label_visibility="collapsed")
                                ans_parts.append("Đ" if choice == "Đúng" else ("S" if choice == "Sai" else ""))
                        else:
                            ans_parts.append("")
                    st.session_state.answers[q_id] = ", ".join(ans_parts)
                
            elif dang == 3:
                st.markdown("<div style='padding: 25px;'>", unsafe_allow_html=True)
                saved_ans = st.session_state.answers.get(q_id, "")
                val = st.text_input(f"> KẾT QUẢ:", value=saved_ans, key=f"ans_{q_id}", placeholder="NHẬP_VÀO_ĐÂY...")
                st.session_state.answers[q_id] = val
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<hr style='border-top: 1px solid #005f66; margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
            
            col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 2, 1])
            with col_btn_1:
                if current_idx > 0:
                    if st.button("⬅ QUAY LẠI", use_container_width=True):
                        st.session_state.current_q_index -= 1
                        st.rerun()
            with col_btn_3:
                if current_idx < total_q - 1:
                    if st.button("TIẾP TỤC ➡", use_container_width=True):
                        st.session_state.current_q_index += 1
                        st.rerun()
                else:
                    if st.button("XÁC NHẬN NỘP BÀI", type="primary", use_container_width=True):
                        st.session_state.trigger_submit = True
                        st.rerun()

    # XỬ LÝ CHẤM ĐIỂM
    if submit_btn or st.session_state.get('trigger_submit', False):
        st.session_state.trigger_submit = False
        diem = 0.0
        diem_d1 = float(st.session_state.config.get("Diem_Moi_Cau_D1", 0.5))
        diem_d2_y = float(st.session_state.config.get("Diem_Moi_Y_D2", 0.5))
        diem_d3 = float(st.session_state.config.get("Diem_Moi_Cau_D3", 3.0))
        chi_tiet_bai_lam = [] 
        
        for i, qu in enumerate(st.session_state.questions):
            dang = int(qu.get('Dang', 0))
            dap_an_dung = str(qu.get('DapAn', '')).replace("$", "").strip().lower()
            hoc_sinh_chon_goc = str(st.session_state.answers.get(qu.get('ID', ''), ""))
            hoc_sinh_chon = hoc_sinh_chon_goc.replace("$", "").strip().lower()
            chi_tiet_bai_lam.append(f"Câu {i+1}: {hoc_sinh_chon_goc if hoc_sinh_chon_goc else 'Bỏ trống'}")
            
            if dang == 1 and hoc_sinh_chon == dap_an_dung: diem += diem_d1
            elif dang == 2:
                hs_arr, da_arr = [x.strip() for x in hoc_sinh_chon.split(",")], [x.strip() for x in dap_an_dung.split(",")]
                for k in range(min(len(hs_arr), len(da_arr))):
                    if hs_arr[k] == da_arr[k] and hs_arr[k] != "": diem += diem_d2_y
            elif dang == 3 and hoc_sinh_chon == dap_an_dung and hoc_sinh_chon != "": diem += diem_d3
                    
        payload = {"hoTen": st.session_state.ho_ten, "lop": st.session_state.lop, "diem": round(diem, 2), "chiTiet": "\n".join(chi_tiet_bai_lam)}
        try: requests.post(API_URL, json=payload)
        except: pass
        st.session_state.final_score = round(diem, 2)
        st.session_state.exam_state = 'SUBMITTED'
        st.rerun()

# ==========================================
# 7. MÀN HÌNH KẾT QUẢ
# ==========================================
elif st.session_state.exam_state == 'SUBMITTED':
    st.balloons()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.write("")
        
        if st.session_state.get('cheat_count', 0) >= 3:
            st.error("🚫 BÀI THI KẾT THÚC DO VI PHẠM QUY CHẾ: Bạn đã bị thu bài do vi phạm gian lận 3 lần.")
            
        st.markdown(f"""
        <div style='background: #050505; border: 2px solid #00f3ff; border-radius: 0px; padding: 50px; text-align: center; box-shadow: 0 0 20px rgba(0,243,255,0.2) inset;'>
            <h2 style="color: #00f3ff; letter-spacing: 3px; font-family: monospace;">TẢI DỮ LIỆU HOÀN TẤT!</h2>
            <p style="color: #94a3b8; font-size: 1.3em; margin-top: 20px; font-family: monospace;">ĐIỂM_SỐ_CỦA_BẠN:</p>
            <h1 style="font-size: 120px; font-weight: 900; color: #d946ef; margin: 10px 0; text-shadow: 0 0 15px rgba(217,70,239,0.5);">
                {st.session_state.final_score} <span style="font-size: 40px; color: #005f66;">/ 10</span>
            </h1>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("VỀ TRANG CHỦ 🔄", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# ==========================================
# 8. FOOTER TÁC GIẢ
# ==========================================
st.markdown("""
<div style='text-align: center; color: #00f3ff; font-size: 15px; font-family: monospace; letter-spacing: 2px; border-top: 1px dashed #005f66; padding-top: 20px; margin-top: 50px;'>
    SYS_ADMIN: TRẦN VĂN LINH
</div>
""", unsafe_allow_html=True)
