document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("questionScoreChart");
    const chartData = window.submissionChartData;
    const modeButtons = Array.from(document.querySelectorAll("[data-chart-mode]"));
    const answerAnchors = Array.from(document.querySelectorAll("[data-question-anchor]"));
    const inspectorContainer = document.querySelector(".chart-inspector");

    const inspector = {
        title: document.getElementById("chartInspectorTitle"),
        question: document.getElementById("chartInspectorQuestion"),
        dimension: document.getElementById("chartInspectorDimension"),
        score: document.getElementById("chartInspectorScore"),
        intensity: document.getElementById("chartInspectorIntensity")
    };

    if (!canvas || !Array.isArray(chartData) || typeof Chart === "undefined") {
        return;
    }

    const palette = {
        1: { fill: "#2f7667", pill: "#1f5d51", label: "Base estável" },
        2: { fill: "#8b9270", pill: "#737956", label: "Observação" },
        3: { fill: "#b07c43", pill: "#925f2e", label: "Atenção clínica" },
        4: { fill: "#a44339", pill: "#87342b", label: "Alta criticidade" }
    };

    const baseOrder = [...chartData];
    let currentData = [...baseOrder];
    let pinnedQuestionNumber = null;
    const chartShell = canvas.parentElement;

    const getSortedData = (mode) => {
        if (mode === "severity") {
            return [...baseOrder].sort((a, b) => {
                if (b.score !== a.score) {
                    return b.score - a.score;
                }
                return a.question_number - b.question_number;
            });
        }

        if (mode === "focus") {
            return [...baseOrder]
                .filter((item) => item.score >= 3)
                .sort((a, b) => {
                    if (b.score !== a.score) {
                        return b.score - a.score;
                    }
                    return a.question_number - b.question_number;
                });
        }

        return [...baseOrder];
    };

    const setInspector = (item, { pinned = false } = {}) => {
        if (!item) {
            return;
        }

        if (inspectorContainer) {
            inspectorContainer.classList.toggle("is-pinned", pinned);
        }

        inspector.title.textContent = `${pinned ? "Fixado" : "Pergunta"} ${item.question_number} · ${item.short_label}`;
        inspector.question.textContent = item.question;
        inspector.dimension.textContent = item.short_label;
        inspector.score.textContent = `${item.score}/4`;
        inspector.intensity.textContent = item.intensity;
    };

    const clearAnswerHighlights = () => {
        answerAnchors.forEach((anchor) => {
            anchor.classList.remove("is-focus");
        });
    };

    const focusAnswer = (questionNumber) => {
        const anchor = document.querySelector(`[data-question-anchor="${questionNumber}"]`);
        if (!anchor) {
            return;
        }

        clearAnswerHighlights();
        anchor.classList.add("is-focus");
        anchor.scrollIntoView({ behavior: "smooth", block: "center" });

        window.setTimeout(() => {
            anchor.classList.remove("is-focus");
        }, 2200);
    };

    const activateModeButton = (mode) => {
        modeButtons.forEach((button) => {
            button.classList.toggle("is-active", button.dataset.chartMode === mode);
        });
    };

    const riskBandsPlugin = {
        id: "riskBandsPlugin",
        beforeDatasetsDraw(chart) {
            const { ctx, chartArea, scales } = chart;
            if (!chartArea || !scales.x) {
                return;
            }

            const bands = [
                { start: 0, end: 1, color: "rgba(47, 118, 103, 0.07)" },
                { start: 1, end: 2, color: "rgba(139, 146, 112, 0.08)" },
                { start: 2, end: 3, color: "rgba(176, 124, 67, 0.08)" },
                { start: 3, end: 4, color: "rgba(164, 67, 57, 0.09)" }
            ];

            ctx.save();
            bands.forEach((band) => {
                const x = scales.x.getPixelForValue(band.start);
                const x2 = scales.x.getPixelForValue(band.end);
                ctx.fillStyle = band.color;
                ctx.fillRect(x, chartArea.top, x2 - x, chartArea.bottom - chartArea.top);
            });
            ctx.restore();
        }
    };

    const valuePillsPlugin = {
        id: "valuePillsPlugin",
        afterDatasetsDraw(chart) {
            const { ctx } = chart;
            const meta = chart.getDatasetMeta(0);

            ctx.save();
            ctx.font = "700 11px Manrope, sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";

            meta.data.forEach((bar, index) => {
                const item = currentData[index];
                if (!item) {
                    return;
                }

                const width = 42;
                const height = 22;
                const x = Math.min(bar.x + 30, chart.chartArea.right - width / 2);
                const y = bar.y;
                const left = x - width / 2;
                const top = y - height / 2;
                const radius = 11;

                ctx.fillStyle = palette[item.score].pill;
                ctx.beginPath();
                ctx.moveTo(left + radius, top);
                ctx.lineTo(left + width - radius, top);
                ctx.quadraticCurveTo(left + width, top, left + width, top + radius);
                ctx.lineTo(left + width, top + height - radius);
                ctx.quadraticCurveTo(left + width, top + height, left + width - radius, top + height);
                ctx.lineTo(left + radius, top + height);
                ctx.quadraticCurveTo(left, top + height, left, top + height - radius);
                ctx.lineTo(left, top + radius);
                ctx.quadraticCurveTo(left, top, left + radius, top);
                ctx.closePath();
                ctx.fill();

                ctx.fillStyle = "#f8f4ee";
                ctx.fillText(`${item.score}/4`, x, y + 0.5);
            });

            ctx.restore();
        }
    };

    const setChartHeight = (itemCount) => {
        if (!chartShell) {
            return;
        }

        const height = Math.max(360, itemCount * 54);
        chartShell.style.height = `${height}px`;
    };

    setChartHeight(baseOrder.length);

    const chart = new Chart(canvas, {
        type: "bar",
        data: {
            labels: baseOrder.map((item) => `P${item.question_number} · ${item.short_label}`),
            datasets: [
                {
                    label: "Pontuação",
                    data: baseOrder.map((item) => item.score),
                    backgroundColor: baseOrder.map((item) => palette[item.score].fill),
                    borderRadius: 999,
                    borderSkipped: false,
                    barThickness: 24,
                    maxBarThickness: 24
                }
            ]
        },
        options: {
            indexAxis: "y",
            maintainAspectRatio: false,
            animation: {
                duration: 500,
                easing: "easeOutQuart"
            },
            interaction: {
                mode: "nearest",
                axis: "y",
                intersect: true
            },
            layout: {
                padding: {
                    right: 56,
                    top: 6,
                    bottom: 6
                }
            },
            onClick: (_, elements) => {
                if (!elements.length) {
                    pinnedQuestionNumber = null;
                    if (currentData[0]) {
                        setInspector(currentData[0]);
                    }
                    return;
                }

                const item = currentData[elements[0].index];
                if (!item) {
                    return;
                }

                pinnedQuestionNumber = item.question_number;
                setInspector(item, { pinned: true });
                focusAnswer(item.question_number);
            },
            onHover: (_, elements) => {
                if (pinnedQuestionNumber !== null) {
                    return;
                }

                if (!elements.length) {
                    if (currentData[0]) {
                        setInspector(currentData[0]);
                    }
                    return;
                }

                const item = currentData[elements[0].index];
                if (item) {
                    setInspector(item);
                }
            },
            scales: {
                x: {
                    min: 0,
                    max: 4,
                    ticks: {
                        stepSize: 1,
                        color: "#57625d",
                        font: {
                            size: 11,
                            weight: "700"
                        }
                    },
                    grid: {
                        color: "rgba(46, 57, 53, 0.09)"
                    },
                    border: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: "Intensidade da resposta",
                        color: "#57625d",
                        font: {
                            size: 12,
                            weight: "700"
                        }
                    }
                },
                y: {
                    ticks: {
                        color: "#1f2724",
                        font: {
                            size: 12,
                            weight: "800"
                        }
                    },
                    grid: {
                        display: false
                    },
                    border: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: "rgba(24, 31, 29, 0.94)",
                    titleFont: {
                        size: 13,
                        weight: "700"
                    },
                    bodyFont: {
                        size: 12
                    },
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        title(items) {
                            const item = currentData[items[0].dataIndex];
                            return `Pergunta ${item.question_number} · ${item.short_label}`;
                        },
                        label(context) {
                            const item = currentData[context.dataIndex];
                            return `${item.score}/4 · ${item.intensity}`;
                        },
                        afterLabel(context) {
                            const item = currentData[context.dataIndex];
                            return item ? item.question : "";
                        },
                        footer(context) {
                            const item = currentData[context[0].dataIndex];
                            return item ? `Clique para abrir a resposta ${item.question_number}.` : "";
                        }
                    }
                }
            }
        },
        plugins: [riskBandsPlugin, valuePillsPlugin]
    });

    const applyMode = (mode) => {
        pinnedQuestionNumber = null;
        currentData = getSortedData(mode);
        setChartHeight(currentData.length);
        chart.data.labels = currentData.map((item) => `P${item.question_number} · ${item.short_label}`);
        chart.data.datasets[0].data = currentData.map((item) => item.score);
        chart.data.datasets[0].backgroundColor = currentData.map((item) => palette[item.score].fill);
        chart.update();

        if (currentData[0]) {
            setInspector(currentData[0]);
        }
    };

    modeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const mode = button.dataset.chartMode || "ordered";
            activateModeButton(mode);
            applyMode(mode);
        });
    });

    canvas.addEventListener("mouseleave", () => {
        if (pinnedQuestionNumber !== null) {
            const pinnedItem = currentData.find((item) => item.question_number === pinnedQuestionNumber);
            if (pinnedItem) {
                setInspector(pinnedItem, { pinned: true });
            }
            return;
        }

        if (currentData[0]) {
            setInspector(currentData[0]);
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") {
            return;
        }

        pinnedQuestionNumber = null;
        if (currentData[0]) {
            setInspector(currentData[0]);
        }
    });

    activateModeButton("ordered");
    applyMode("ordered");

    // ============================================
    // GRÁFICO DE NÍVEIS RN1 PROFISSIONAL
    // ============================================
    const rn1Canvas = document.getElementById("rn1LevelsChart");
    if (rn1Canvas && chartData) {
        const totalScore = chartData.reduce((sum, item) => sum + item.score, 0);
        
        // Definir níveis RN1 com faixas corretas
        const levels = [
            { name: "Nível 1", min: 10, max: 15, color: "#2f7667", label: "Relacionamento Saudável" },
            { name: "Nível 2", min: 16, max: 25, color: "#8b9270", label: "Sinais de Alerta" },
            { name: "Nível 3", min: 26, max: 35, color: "#b07c43", label: "Relacionamento Tóxico" },
            { name: "Nível 4", min: 36, max: 40, color: "#a44339", label: "Abuso Narcisista Severo" }
        ];

        // Encontrar nível atual do paciente
        let currentLevel = levels[0];
        for (const level of levels) {
            if (totalScore >= level.min && totalScore <= level.max) {
                currentLevel = level;
                break;
            }
        }

        // Calcular posição percentual dentro do nível
        const levelRange = currentLevel.max - currentLevel.min;
        const positionInLevel = totalScore - currentLevel.min;
        const percentInLevel = (positionInLevel / levelRange) * 100;

        new Chart(rn1Canvas, {
            type: "bar",
            data: {
                labels: levels.map(l => `${l.name}\n${l.min}-${l.max} pts`),
                datasets: [{
                    label: "Amplitude do Nível",
                    data: levels.map(l => l.max - l.min + 1),
                    backgroundColor: levels.map(l => {
                        if (l.name === currentLevel.name) {
                            return l.color;
                        }
                        return `${l.color}20`;
                    }),
                    borderColor: levels.map(l => l.color),
                    borderWidth: levels.map(l => l.name === currentLevel.name ? 4 : 2),
                    borderRadius: 16,
                    barThickness: 60
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        right: 80,
                        left: 20,
                        top: 10,
                        bottom: 10
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: "rgba(24, 31, 29, 0.96)",
                        titleFont: { size: 15, weight: "700" },
                        bodyFont: { size: 13 },
                        padding: 16,
                        displayColors: false,
                        callbacks: {
                            title: (items) => {
                                const level = levels[items[0].dataIndex];
                                return `${level.name} (${level.min}-${level.max} pontos)`;
                            },
                            label: (context) => {
                                const level = levels[context.dataIndex];
                                if (level.name === currentLevel.name) {
                                    return [
                                        `✓ PACIENTE ESTÁ AQUI`,
                                        `Pontuação: ${totalScore} pontos`,
                                        `Posição: ${percentInLevel.toFixed(0)}% dentro do nível`
                                    ];
                                }
                                return level.label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: false,
                        max: 12
                    },
                    y: {
                        ticks: {
                            color: "#1f2724",
                            font: { size: 13, weight: "800" },
                            padding: 10
                        },
                        grid: { display: false },
                        border: { display: false }
                    }
                }
            },
            plugins: [{
                id: "patientScoreMarker",
                afterDatasetsDraw(chart) {
                    const { ctx } = chart;
                    const levelIndex = levels.findIndex(l => l.name === currentLevel.name);
                    if (levelIndex === -1) return;

                    const meta = chart.getDatasetMeta(0);
                    const bar = meta.data[levelIndex];
                    
                    // Calcular posição exata do marcador dentro da barra
                    const barWidth = bar.width;
                    const markerPosition = (positionInLevel / levelRange) * barWidth;
                    const markerX = bar.x - (barWidth / 2) + markerPosition;
                    const markerY = bar.y;

                    ctx.save();
                    
                    // Linha vertical indicadora
                    ctx.beginPath();
                    ctx.moveTo(markerX, markerY - 35);
                    ctx.lineTo(markerX, markerY + 35);
                    ctx.strokeStyle = "#fff";
                    ctx.lineWidth = 3;
                    ctx.stroke();

                    // Círculo com pontuação
                    ctx.beginPath();
                    ctx.arc(markerX, markerY, 32, 0, Math.PI * 2);
                    ctx.fillStyle = currentLevel.color;
                    ctx.fill();
                    ctx.strokeStyle = "#fff";
                    ctx.lineWidth = 4;
                    ctx.stroke();

                    // Texto da pontuação
                    ctx.fillStyle = "#fff";
                    ctx.font = "700 18px Manrope, sans-serif";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(totalScore, markerX, markerY);

                    // Label "VOCÊ ESTÁ AQUI"
                    ctx.fillStyle = currentLevel.color;
                    ctx.font = "800 11px Manrope, sans-serif";
                    ctx.fillText("PACIENTE", markerX, markerY - 50);

                    ctx.restore();
                }
            }]
        });
    }
});
