import streamlit as st

st.set_page_config(page_title="🎲 Baccarat Web Predictor", layout="centered")
st.title("🎲 Baccarat Predictor Web")

if "history" not in st.session_state:
    st.session_state.history = []

entry = st.text_input("Nhập kết quả (B/P/T)", max_chars=1).upper()
if st.button("➕ Thêm") and entry in ["B","P","T"]:
    st.session_state.history.append(entry)
if st.button("🔄 Reset"):
    st.session_state.history.clear()

st.subheader("📜 Lịch sử:")
st.write(" ".join(st.session_state.history) if st.session_state.history else "(chưa có)")

# Big Road
def big_road(h):
    road=[]; curr=None; col=[]
    for v in h:
        if v=="T": continue
        if v==curr: col.append(v)
        else:
            if col: road.append(col)
            col=[v]; curr=v
    if col: road.append(col)
    return road

road = big_road(st.session_state.history)
st.subheader("📈 Big Road:")
for i,c in enumerate(road):
    st.write(f"Cột {i+1}: {' → '.join(c)}")

# Xác suất & prediction
if len(st.session_state.history)>=5:
    recent = st.session_state.history[-10:]
    b=recent.count("B"); p=recent.count("P"); t=recent.count("T")
    total=b+p+t
    pct=(lambda x: round(x*100/total,1))
    pctB,pctP,pctT = pct(b),pct(p),pct(t)
    best = max([("Banker",pctB),("Player",pctP),("Tie",pctT)], key=lambda x: x[1])[0]
    last = road[-1] if road else []
    trend = last[0] if last else "-"
    guess = f"🔁 Theo trend: tiếp tục '{trend}'" if len(last)>=3 else "⚠️ Dự đoán đổi bên"
    st.subheader("💡 Dự đoán & Xác suất:")
    st.write(f"- Dự đoán: **{best}**")
    st.write(f"- Tỷ lệ 10 ván gần nhất: Banker {pctB}%, Player {pctP}%, Tie {pctT}%")
    st.write(f"- {guess}")
else:
    st.subheader("⏳ Cần ít nhất 5 kết quả để phân tích.")
