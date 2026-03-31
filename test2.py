import streamlit as st

st.set_page_config(
    page_title="Instagram Cube Stories",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("📱 Instagram Stories Cube Transition")
st.markdown("**Drag/swipe** left or right • Auto advances every 5 seconds")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IG Cube Stories</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        body { margin:0; padding:0; background:#000; font-family:'Inter',sans-serif; }
        
        .stories-container {
            width: 380px;
            height: 620px;
            background: #111;
            border-radius: 20px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 40px rgba(0,0,0,0.9);
            touch-action: none;
            user-select: none;
        }
        
        .top-bar {
            position: absolute; top: 0; left: 0; right: 0;
            height: 50px; background: rgba(0,0,0,0.6); z-index: 100;
            display: flex; align-items: center; padding: 0 15px; gap: 10px;
        }
        
        .progress-bar { flex: 1; height: 3px; background: rgba(255,255,255,0.4); border-radius: 2px; overflow: hidden; }
        .progress { height: 100%; background: white; width: 25%; transition: width 0.3s linear; }
        
        .scene { width: 100%; height: 100%; perspective: 1400px; position: relative; }
        
        .cube {
            width: 100%; height: 100%;
            position: absolute;
            transform-style: preserve-3d;
            transition: transform 0.5s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        
        .face {
            position: absolute; width: 100%; height: 100%;
            backface-visibility: hidden; overflow: hidden;
        }
        .face img { width: 100%; height: 100%; object-fit: cover; }
        
        .face-front  { transform: rotateY(0deg) translateZ(190px); }
        .face-right  { transform: rotateY(90deg) translateZ(190px); }
        .face-back   { transform: rotateY(180deg) translateZ(190px); }
        .face-left   { transform: rotateY(-90deg) translateZ(190px); }
        
        .story-overlay {
            position: absolute; bottom: 0; left: 0; right: 0;
            padding: 25px 20px;
            background: linear-gradient(transparent, rgba(0,0,0,0.9));
            z-index: 10;
        }
    </style>
</head>
<body>
    <div class="stories-container" id="container">
        <div class="top-bar">
            <div class="progress-bar"><div class="progress" id="progress"></div></div>
            <span style="font-size:22px; font-weight:600; opacity:0.8;">×</span>
        </div>
        
        <div class="scene">
            <div class="cube" id="cube">
                <div class="face face-front"><img src="https://picsum.photos/id/1015/800/1200"></div>
                <div class="face face-right"><img src="https://picsum.photos/id/237/800/1200"></div>
                <div class="face face-back"><img src="https://picsum.photos/id/866/800/1200"></div>
                <div class="face face-left"><img src="https://picsum.photos/id/201/800/1200"></div>
            </div>
        </div>
        
        <div class="story-overlay">
            <div style="display:flex; align-items:center; gap:12px;">
                <img src="https://picsum.photos/id/64/200/200" style="width:42px;height:42px;border-radius:50%;border:2.5px solid white;">
                <div>
                    <div style="font-weight:600;">nocodile</div>
                    <div style="font-size:13px;opacity:0.8;">2h ago</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const cube = document.getElementById('cube');
        const container = document.getElementById('container');
        let currentIndex = 0;
        const total = 4;
        let startX = 0;
        let isDragging = false;

        function updateCube() {
            const rotation = currentIndex * -90;
            cube.style.transform = `rotateY(${rotation}deg)`;
            document.getElementById('progress').style.width = 
                `${((currentIndex % total) + 1) / total * 100}%`;
        }

        // ============== MOUSE & TOUCH SWIPE ==============
        container.addEventListener('mousedown', e => {
            isDragging = true;
            startX = e.clientX;
            cube.style.transition = 'none';
        });

        container.addEventListener('mousemove', e => {
            if (!isDragging) return;
            const diff = e.clientX - startX;
            const liveRotation = currentIndex * -90 + (diff * 0.5);
            cube.style.transform = `rotateY(${liveRotation}deg)`;
        });

        container.addEventListener('mouseup', e => {
            if (!isDragging) return;
            finishSwipe(e.clientX);
        });

        container.addEventListener('mouseleave', () => {
            if (isDragging) finishSwipe(startX); // cancel if mouse leaves
        });

        // Touch Support
        container.addEventListener('touchstart', e => {
            isDragging = true;
            startX = e.touches[0].clientX;
            cube.style.transition = 'none';
        }, { passive: true });

        container.addEventListener('touchmove', e => {
            if (!isDragging) return;
            const diff = e.touches[0].clientX - startX;
            const liveRotation = currentIndex * -90 + (diff * 0.5);
            cube.style.transform = `rotateY(${liveRotation}deg)`;
        }, { passive: true });

        container.addEventListener('touchend', e => {
            if (!isDragging) return;
            finishSwipe(e.changedTouches[0].clientX);
        });

        function finishSwipe(endX) {
            isDragging = false;
            const diff = startX - endX;
            
            if (diff > 70) {
                currentIndex = (currentIndex + 1) % total;        // Swipe Left
            } else if (diff < -70) {
                currentIndex = (currentIndex - 1 + total) % total; // Swipe Right
            }
            
            cube.style.transition = 'transform 0.5s cubic-bezier(0.25, 0.1, 0.25, 1)';
            updateCube();
        }

        // Keyboard
        document.addEventListener('keydown', e => {
            if (e.key === 'ArrowRight') currentIndex = (currentIndex + 1) % total;
            if (e.key === 'ArrowLeft') currentIndex = (currentIndex - 1 + total) % total;
            updateCube();
        });

        // Auto advance
        setInterval(() => {
            currentIndex = (currentIndex + 1) % total;
            updateCube();
        }, 5000);

        // Init
        updateCube();
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=680, width=400, scrolling=False)

st.success("✅ Fixed: Now only tracks mouse **while pressing/dragging**")
st.info("Try clicking and dragging left/right on the story area")