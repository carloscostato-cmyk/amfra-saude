document.addEventListener("DOMContentLoaded", () => {
    // ========================================
    // 🎨 Agent UX/UI - Botão Copiar Melhorado
    // ========================================
    const copyBtn = document.getElementById("copyLinkBtn");
    if (copyBtn) {
        copyBtn.addEventListener("click", async () => {
            const text = copyBtn.getAttribute("data-copy-text");
            if (!text) return;

            try {
                await navigator.clipboard.writeText(text);
                const btnText = copyBtn.querySelector(".btn-text");
                const btnCopied = copyBtn.querySelector(".btn-text-copied");
                
                btnText.style.display = "none";
                btnCopied.style.display = "inline";
                copyBtn.style.background = "#10b981";
                
                setTimeout(() => {
                    btnText.style.display = "inline";
                    btnCopied.style.display = "none";
                    copyBtn.style.background = "";
                }, 2000);
            } catch (error) {
                console.error("Erro ao copiar:", error);
                alert("Não foi possível copiar o link");
            }
        });
    }

    // Fallback para botões antigos
    document.querySelectorAll("[data-copy-text]").forEach((button) => {
        if (button.id === "copyLinkBtn") return; // Skip the new button
        
        button.addEventListener("click", async () => {
            const text = button.getAttribute("data-copy-text");
            if (!text) return;

            try {
                await navigator.clipboard.writeText(text);
                const originalText = button.textContent;
                button.textContent = "✓ Copiado!";
                setTimeout(() => {
                    button.textContent = originalText;
                }, 1800);
            } catch (error) {
                console.error("Não foi possível copiar o texto.", error);
            }
        });
    });

    // ========================================
    // 📸 Agent Camera - Captura de Foto
    // ========================================
    const startCameraBtn = document.getElementById("startCamera");
    const capturePhotoBtn = document.getElementById("capturePhoto");
    const retakePhotoBtn = document.getElementById("retakePhoto");
    const camera = document.getElementById("camera");
    const photoCanvas = document.getElementById("photoCanvas");
    const photoPreview = document.getElementById("photoPreview");
    const photoData = document.getElementById("photoData");
    
    let stream = null;

    if (startCameraBtn) {
        startCameraBtn.addEventListener("click", async () => {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "user", width: 640, height: 480 } 
                });
                camera.srcObject = stream;
                camera.style.display = "block";
                startCameraBtn.style.display = "none";
                capturePhotoBtn.style.display = "inline-block";
            } catch (error) {
                console.error("Erro ao acessar câmera:", error);
                alert("Não foi possível acessar a câmera. Verifique as permissões.");
            }
        });
    }

    if (capturePhotoBtn) {
        capturePhotoBtn.addEventListener("click", () => {
            const context = photoCanvas.getContext("2d");
            photoCanvas.width = camera.videoWidth;
            photoCanvas.height = camera.videoHeight;
            context.drawImage(camera, 0, 0);
            
            const imageData = photoCanvas.toDataURL("image/jpeg", 0.8);
            photoData.value = imageData;
            photoPreview.src = imageData;
            photoPreview.style.display = "block";
            
            camera.style.display = "none";
            capturePhotoBtn.style.display = "none";
            retakePhotoBtn.style.display = "inline-block";
            
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        });
    }

    if (retakePhotoBtn) {
        retakePhotoBtn.addEventListener("click", async () => {
            photoPreview.style.display = "none";
            photoData.value = "";
            retakePhotoBtn.style.display = "none";
            
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "user", width: 640, height: 480 } 
                });
                camera.srcObject = stream;
                camera.style.display = "block";
                capturePhotoBtn.style.display = "inline-block";
            } catch (error) {
                console.error("Erro ao reabrir câmera:", error);
                startCameraBtn.style.display = "inline-block";
            }
        });
    }
});
