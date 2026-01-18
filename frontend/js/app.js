// 2026-01-16: Vue.js 초기화 - 챕터 데이터 관리 및 UI 인터랙션 정의
// [Role: 프론트엔드 비즈니스 로직, 상태 관리 및 API 통신 제어]
const { createApp } = Vue;

const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            userProteinShakes: 420,
            chapters: [],
            leaderboard: [
                { id: 1, username: 'TopEngineer', solved: 45, shakes: 2450 },
                { id: 2, username: 'DjangoMaster', solved: 42, shakes: 2100 },
                { id: 3, username: 'VueNinja', solved: 38, shakes: 1850 },
                { id: 4, username: 'AgentZero', solved: 35, shakes: 1600 },
                { id: 5, username: 'OpsWizard', solved: 30, shakes: 1400 }
            ],
            // 2026-01-16: Agent Workspace 상태 관리를 위한 데이터 필드 추가
            isAgentModalOpen: false,
            isReportModalOpen: false, // 상세 리포트 창 상태
            activeProblem: null,
            editedPrompt: '',
            submissionResult: null,
            // 2026-01-16: Live Chat Playground 데이터 추가
            chatHistory: [],
            userInput: '',
            isTyping: false,
            // 2026-01-17: 새 보안 공지사항 강조를 위해 페이지 로드 시 자동 노출 설정
            isNoticeOpen: true,
            // 로그인 모달 상태
            isLoginModalOpen: false,
            loginEmail: '',
            loginPassword: '',

            // 회원가입 모달 상태 (Antigravity Design)
            isSignUpModalOpen: false,
            isSignUpSuccessOpen: false,
            signupNickname: '',
            signupEmail: '',
            signupPassword: '',
            signupBirthDate: '',
            signupIsDeveloper: false,
            signupJobRole: '',
            signupInterests: [],
            signupAgreed: false,
            signupCustomInterest: '',
            availableInterests: ['System Design', 'Cloud', 'Cybersecurity', 'Database', 'Mobile', 'UI/UX'],

            // 로그인 정보 (신원 확인용)
            isLoggedIn: false,
            sessionNickname: '',

            // Unit 팝업 관리
            isUnitModalOpen: false,
            activeUnit: null,
            activeChapter: null,
            showScrollHint: false,
            scrollHintTimeout: null,

            // Mermaid 팝업 관리 (Unit 2 전용)
            isMermaidModalOpen: false,
            mermaidCode: 'graph TD\n    A[Start] --> B{Is it working?}\n    B -- Yes --> C[Great!]\n    B -- No --> D[Debug It]',
            mermaidHintVisible: false,
            mermaidEvaluation: null,

            // Debug Gym Sandbox State (Unit 2)
            isDebugModalOpen: false,
            debugFiles: [
                { name: 'main.py', content: 'from auth import login\n\ndef main():\n    user = {"id": 1, "username": "admin"}\n    if login(user):\n        print("Login success")\n    else:\n        print("Login failed")\n\nif __name__ == "__main__":\n    main()' },
                { name: 'auth.py', content: 'from cache import get_token, is_valid_token\n\ndef login(user):\n    """\n    Authenticate user by checking their cached token.\n    BUG: Incorrectly validates the token - compares with wrong field.\n    """\n    user_id = user["id"]\n    token = get_token(user_id)\n\n    if token is None:\n        return False\n\n    # BUG: Should check is_valid_token(token, user_id) but checks with username instead\n    return is_valid_token(token, user)\n' },
                { name: 'cache.py', content: 'def get_token(user_id):\n    # Simulate getting token\n    return "abc-123"\n\ndef is_valid_token(token, user):\n    # Simplified validation\n    return token == "abc-123" and user.get("id") == 1' },
                { name: 'users.json', content: '[\n    {"id": 1, "username": "admin"}\n]' }
            ],
            activeDebugFile: null,
            debugTerminalOutput: 'Ready to run.',
            debugEventLogs: [],

            // Code Practice State (Unit 1)
            isCodeModalOpen: false,
            codeStep: 'upload', // 'upload' | 'result'
            codeEvaluation: null, // Test results
            unit1Code: `from typing import Dict, Optional
from datetime import datetime

class RateLimiter:
    def __init__(self):
        self.org_counters: Dict[str, int] = {}
        self.user_counters: Dict[str, int] = {}
        self.current_second: int = 0

    def process_request(self, event: dict) -> str:
        # 요응 직면
        # Args: {`,

            // Chart.js 인스턴스
            performanceChart: null,

            // 제출 중 로딩 상태
            isSubmitting: false,

            // 추가: 로그인 권한 확인 모달 상태
            isAuthRequiredModalOpen: false,

            // 2026-01-17: 선택된 챕터 상태 관리를 위한 필드 추가 (정리됨)

            // 2026-01-17: Pseudo-Code Playground (Unit 6) State
            isPseudoModalOpen: false,
            pseudoCode: 'FOR i FROM 1 TO 5 DO\n  PRINT "Hello World"\nEND FOR',
            pseudoOutput: [],
            isPseudoRunning: false
        }
    },
    methods: {
        async fetchChapters() {
            try {
                const response = await fetch('/api/chapters/');
                const data = await response.json();

                // 2026-01-16: 디자인 시스템을 위한 색상 보충
                const colors = ['#58cc02', '#1cb0f6', '#ff9600', '#ce82ff', '#ff4b4b'];
                const iconMap = {
                    'Code Practice': 'code',
                    'Debug Practice': 'bug',
                    'System Practice': 'layers',
                    'Ops Practice': 'zap',
                    'Agent Practice': 'bot',
                    'Pseudo Practice': 'gamepad-2'
                };

                this.chapters = data.map((ch, idx) => ({
                    ...ch,
                    color: colors[idx % colors.length],
                    icon: iconMap[ch.name] || 'book'
                }));

                this.$nextTick(() => {
                    if (window.lucide) window.lucide.createIcons();
                });
            } catch (error) {
                console.error('Failed to fetch chapters:', error);
            }
        },
        closeNotice() {
            this.isNoticeOpen = false;
            this.$nextTick(() => {
                if (window.lucide) window.lucide.createIcons();
            });
        },
        getIconForChapter(name) {
            const icons = {
                'Code Practice': 'code',
                'Debug Practice': 'bug',
                'System Practice': 'layers',
                'Ops Practice': 'zap',
                'Agent Practice': 'bot',
                'Pseudo Practice': 'gamepad-2'
            };
            return icons[name] || 'book';
        },
        getColorForChapter(name) {
            const colors = {
                'Code Practice': '#3b82f6',
                'Debug Practice': '#ef4444',
                'System Practice': '#8b5cf6',
                'Ops Practice': '#f59e0b',
                'Agent Practice': '#10b981',
                'Pseudo Practice': '#ec4899'
            };
            return colors[name] || '#64748b';
        },
        labelsCount(unit) {
            const currentCount = unit?.problems?.length || 0;
            return Math.max(0, 6 - currentCount);
        },
        openUnitPopup(unit) {
            if (!this.isLoggedIn) {
                this.isAuthRequiredModalOpen = true;
                return;
            }
            this.activeUnit = unit;
            this.isUnitModalOpen = true;
            this.$nextTick(() => {
                if (window.lucide) window.lucide.createIcons();
            });
        },
        // 2026-01-17: 문제 선택 로직 고도화 - 챕터별 정확한 워크스페이스 연결 및 상태 관리
        selectProblem(problem, chapter) {
            console.log("Selecting problem:", problem, "in chapter:", chapter);

            if (!this.isLoggedIn) {
                this.isAuthRequiredModalOpen = true;
                return;
            }

            if (!problem) {
                console.error("Problem is null or undefined");
                return;
            }

            this.activeProblem = problem;
            this.activeChapter = chapter; // 2026-01-17: 컨텍스트 유지를 위해 명시적 저장

            // chapter가 객체가 아니라 activeUnit에서 가져와야 할 수도 있음
            const chapterToUse = chapter || this.activeUnit;
            const chapterName = chapterToUse?.name || '';

            console.log("Chapter name:", chapterName);

            if (chapterName.includes('Agent Practice') || chapterName === 'Agent Practice') {
                this.openAgentWorkspace(problem);
            } else if (chapterName.includes('System Practice') || chapterName === 'System Practice') {
                this.isMermaidModalOpen = true;
                this.$nextTick(() => {
                    this.renderMermaid();
                    if (window.lucide) window.lucide.createIcons();
                });
            } else if (chapterName.includes('Ops Practice') || chapterName === 'Ops Practice') {
                // Ops Practice도 현재는 Agent 기반 워크스페이스 사용
                this.openAgentWorkspace(problem);
            } else if (chapterName.includes('Debug Practice') || chapterName === 'Debug Practice') {
                this.openDebugWorkspace(problem);
            } else if (chapterName.includes('Code Practice') || chapterName === 'Code Practice') {
                this.openCodeWorkspace(problem);
            } else if (chapterName.includes('Pseudo Practice') || chapterName === 'Pseudo Practice') {
                this.openPseudoWorkspace(problem);
            } else {
                console.warn("Unknown chapter or area under construction:", chapterName);
                alert(`${chapterName || '해당'} 구역은 현재 준비 중입니다!`);
            }
        },

        // --- Pseudo-Code Practice Methods (Unit 6) ---
        openPseudoWorkspace(problem) {
            this.activeProblem = problem;
            this.isPseudoModalOpen = true;
            this.$nextTick(() => {
                if (window.lucide) window.lucide.createIcons();
            });
        },
        closePseudoWorkspace() {
            this.isPseudoModalOpen = false;
        },
        runPseudoCode() {
            this.isPseudoRunning = true;
            this.pseudoOutput = [];

            // 시뮬레이션 로직
            setTimeout(() => {
                for (let i = 0; i < 5; i++) {
                    this.pseudoOutput.push("Hello World");
                }
                this.isPseudoRunning = false;
                alert("코드 실행 완료! 🎯");
                this.userProteinShakes += 30;
            }, 1000);
        },
        resetPseudoCode() {
            this.pseudoCode = 'FOR i FROM 1 TO 5 DO\n  PRINT "Hello World"\nEND FOR';
        },

        // --- Workspaces ---
        openAgentWorkspace(problem) {
            this.activeProblem = problem;
            this.editedPrompt = problem.agent_info ? problem.agent_info.base_system_prompt : '';
            this.isAgentModalOpen = true;
            this.submissionResult = null;
            this.chatHistory = [];
            this.userInput = '';
            this.$nextTick(() => {
                if (window.lucide) window.lucide.createIcons();
                setTimeout(() => this.initChart(), 100);
            });
        },
        closeAgentWorkspace() {
            this.isAgentModalOpen = false;
        },

        // --- Agent Practice Methods ---
        async sendLiveMessage() {
            if (!this.userInput.trim() || this.isTyping) return;

            const message = this.userInput.trim();
            this.userInput = '';

            // 사용자 메시지 추가
            this.chatHistory.push({
                role: 'user',
                content: message
            });

            // 스크롤 하단으로
            this.$nextTick(() => {
                const chatScroll = this.$refs.chatScroll;
                if (chatScroll) chatScroll.scrollTop = chatScroll.scrollHeight;
            });

            // 타이핑 인디케이터 표시
            this.isTyping = true;

            try {
                // 시뮬레이션: 실제로는 백엔드 API 호출 (프롬프트 + 사용자 메시지)
                await new Promise(resolve => setTimeout(resolve, 1000));

                // 가상 AI 응답
                const responses = [
                    'Based on your system prompt, I can help you with that task.',
                    'I understand your request. Let me process that information.',
                    'That\'s an interesting question! Here\'s what I think...',
                    'Thank you for your message. I\'m here to assist you.',
                    'I\'ve analyzed your input and here are my findings.'
                ];

                this.chatHistory.push({
                    role: 'assistant',
                    content: responses[Math.floor(Math.random() * responses.length)]
                });

                // 스크롤 하단으로
                this.$nextTick(() => {
                    const chatScroll = this.$refs.chatScroll;
                    if (chatScroll) chatScroll.scrollTop = chatScroll.scrollHeight;
                });
            } catch (error) {
                console.error('Chat error:', error);
            } finally {
                this.isTyping = false;
            }
        },

        async submitAgent() {
            if (!this.activeProblem) {
                console.error("No active problem for submission");
                return;
            }

            this.isSubmitting = true;
            try {
                // 시뮬레이션: 실제로는 백엔드 API 호출
                await new Promise(resolve => setTimeout(resolve, 2000));

                // 가상 평가 결과 생성
                this.submissionResult = {
                    accuracy: Math.floor(Math.random() * 20) + 75, // 75-95
                    hallucination_rate: Math.floor(Math.random() * 15) + 5, // 5-20
                    latency: (Math.random() * 1.5 + 0.5).toFixed(2), // 0.5-2.0
                    feedback_message: '프롬프트가 효과적으로 작성되었습니다. 추가적인 제약 조건을 명시하면 더욱 향상될 수 있습니다.'
                };

                this.userProteinShakes += 25;
                this.isAgentModalOpen = false;

                // 모달 전환 후 리포트 모달 열기
                this.$nextTick(() => {
                    this.isReportModalOpen = true;
                });
            } catch (error) {
                console.error('Submit agent error:', error);
                alert('제출 중 오류가 발생했습니다.');
            } finally {
                this.isSubmitting = false;
            }
        },

        openDebugWorkspace(problem) {
            this.activeProblem = problem;
            this.isDebugModalOpen = true;
            this.activeDebugFile = this.debugFiles[1];
            this.debugTerminalOutput = 'Type "python main.py" or click Run to start...';
            this.debugEventLogs = [{ time: '오후 2:00:00', event: 'BOOT', detail: 'System Ready', status: 'neutral' }];
        },
        closeDebugModal() { this.isDebugModalOpen = false; },
        openCodeWorkspace(problem) {
            this.activeProblem = problem;
            this.isCodeModalOpen = true;
            this.codeStep = 'upload';
        },
        closeCodeModal() { this.isCodeModalOpen = false; },

        // --- Code Practice Methods ---
        async runCodeTest() {
            if (!this.unit1Code.trim()) {
                alert('코드를 입력해주세요.');
                return;
            }

            this.isSubmitting = true;
            try {
                // 시뮬레이션: 실제로는 백엔드 API 호출
                await new Promise(resolve => setTimeout(resolve, 2000));

                // 가상 평가 결과
                this.codeEvaluation = {
                    performance: {
                        total: '30,000',
                        allowed: '27,500',
                        denied: '2,500',
                        error: '0',
                        time: '1.85초'
                    },
                    phases: [
                        { name: 'Phase 1', denied_rate: '1.50%' },
                        { name: 'Phase 2', denied_rate: '23.33%' },
                        { name: 'Phase 3', denied_rate: '11.00%' }
                    ],
                    quality: {
                        score: 85,
                        level: 'Mid-Senior',
                        grade: 'A'
                    }
                };

                this.codeStep = 'result';
                this.userProteinShakes += 15;
            } catch (error) {
                console.error('Code test error:', error);
                alert('테스트 실행 중 오류가 발생했습니다.');
            } finally {
                this.isSubmitting = false;
            }
        },

        // --- Debug Practice Methods ---
        selectDebugFile(file) {
            this.activeDebugFile = file;
        },

        // --- System Practice Methods ---
        updateMermaid() {
            // Mermaid 코드가 변경될 때마다 미리보기 업데이트
            this.$nextTick(() => {
                try {
                    const previewElement = document.getElementById('mermaid-preview');
                    if (previewElement && this.mermaidCode.trim()) {
                        previewElement.innerHTML = this.mermaidCode;
                        mermaid.run({
                            querySelector: '#mermaid-preview',
                            suppressErrors: true
                        });
                    }
                } catch (error) {
                    console.error('Mermaid rendering error:', error);
                }
            });
        },
        closeMermaidModal() {
            this.isMermaidModalOpen = false;
        },
        async saveMermaidDesign() {
            if (!this.mermaidCode.trim()) {
                alert('Mermaid 코드를 입력해주세요.');
                return;
            }

            this.isSubmitting = true;
            try {
                // 시뮬레이션: 실제로는 백엔드 API 호출
                await new Promise(resolve => setTimeout(resolve, 1500));

                // 가상 평가 결과 생성 (HTML 템플릿 구조에 맞춤)
                this.mermaidEvaluation = {
                    availability: {
                        score: Math.floor(Math.random() * 2) + 4, // 4-5
                        label: '우수'
                    },
                    security: {
                        score: Math.floor(Math.random() * 2) + 4, // 4-5
                        label: '우수'
                    },
                    performance: {
                        score: Math.floor(Math.random() * 2) + 4, // 4-5
                        label: '우수'
                    },
                    summary: '설계하신 아키텍처는 전반적으로 우수한 수준입니다. 마이크로서비스 간 통신 최적화와 캐시 전략을 보완하면 더욱 향상될 것입니다.'
                };

                this.userProteinShakes += 20;
                alert('아키텍처 디자인이 저장되었습니다! 🎉');
            } catch (error) {
                console.error('Save mermaid error:', error);
                alert('저장 중 오류가 발생했습니다.');
            } finally {
                this.isSubmitting = false;
            }
        },

        // --- Debug Practice Methods ---
        async runDebugCode() {
            this.debugTerminalOutput = 'Running main.py...\n';
            this.debugEventLogs.push({
                time: new Date().toLocaleTimeString('ko-KR'),
                event: 'RUN_SUBMIT',
                detail: 'Executing main.py',
                status: 'neutral'
            });

            await new Promise(resolve => setTimeout(resolve, 1000));

            this.debugTerminalOutput += 'Traceback (most recent call last):\n';
            this.debugTerminalOutput += '  File "main.py", line 5, in <module>\n';
            this.debugTerminalOutput += '    if login(user):\n';
            this.debugTerminalOutput += '  File "auth.py", line 15, in login\n';
            this.debugTerminalOutput += '    return is_valid_token(token, user)\n';
            this.debugTerminalOutput += 'TypeError: is_valid_token() takes 2 positional arguments but 1 was given\n';

            this.debugEventLogs.push({
                time: new Date().toLocaleTimeString('ko-KR'),
                event: 'RUN_SUBMIT',
                detail: 'Execution failed',
                status: 'failure'
            });
        },

        // --- Chart & Metrics ---
        initChart() {
            const ctx = document.getElementById('performanceChart');
            if (!ctx) return;
            if (this.performanceChart) this.performanceChart.destroy();
            this.performanceChart = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Accuracy', 'Hallucination', 'Latency', 'Safety', 'Reliability'],
                    datasets: [{
                        label: 'Current Performance',
                        data: [0, 0, 0, 0, 0],
                        backgroundColor: 'rgba(99, 102, 241, 0.2)',
                        borderColor: '#6366f1',
                        borderWidth: 2
                    }]
                },
                options: {
                    scales: { r: { ticks: { display: false, max: 100, min: 0 } } },
                    plugins: { legend: { display: false } },
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        },
        updateChart(metrics) {
            if (!this.performanceChart || !metrics) return;
            const hScore = Math.max(0, 100 - (metrics.hallucination_rate || 0));
            const lScore = Math.max(0, 100 - ((metrics.latency || 0) * 20));
            this.performanceChart.data.datasets[0].data = [metrics.accuracy || 0, hScore, lScore, 85, 90];
            this.performanceChart.update();
        },

        // --- Auth handlers ---
        handleLogin() { this.isLoginModalOpen = true; },
        completeLogin() {
            if (!this.loginEmail || !this.loginPassword) return alert('입력 필요');
            this.isLoggedIn = true;
            this.isLoginModalOpen = false;
            this.sessionNickname = this.loginEmail.split('@')[0];
        },
        handleSignUp() { this.isSignUpModalOpen = true; },
        completeSignUp() {
            this.isSignUpModalOpen = false;
            this.isSignUpSuccessOpen = true;
        },
        closeSuccessModal() {
            this.isSignUpSuccessOpen = false;
            this.isLoggedIn = true;
            this.sessionNickname = this.signupNickname || 'User';
        },
        handleLogout() {
            this.isLoggedIn = false;
            this.sessionNickname = '';
        },

        // --- Other logic ---
        renderMermaid() {
            if (!window.mermaid) return;
            const element = document.getElementById('mermaid-preview');
            if (element) {
                element.innerHTML = `<div class="mermaid">${this.mermaidCode}</div>`;
                mermaid.init(undefined, '.mermaid');
            }
        },
        handleGoToPlayground() {
            if (this.isLoggedIn) {
                document.getElementById('chapters')?.scrollIntoView({ behavior: 'smooth' });
            } else {
                this.isAuthRequiredModalOpen = true;
            }
        }
    },
    computed: {
        unitBadge() {
            // Agent Workspace 상단에 표시할 배지 텍스트
            if (this.activeChapter) {
                return this.activeChapter.name || 'Practice';
            }
            if (this.activeUnit) {
                return this.activeUnit.name || 'Practice';
            }
            return 'Practice';
        },
        editorLabel() {
            // Agent Workspace 에디터 라벨
            return 'SYSTEM PROMPT EDITOR';
        },
        editorPlaceholder() {
            // Agent Workspace 에디터 플레이스홀더
            return 'You are a helpful AI assistant specialized in...';
        },
        playgroundTitle() {
            // Chat Playground 타이틀
            return 'LIVE CHAT PLAYGROUND';
        },
        emptyChatMessage() {
            // 채팅이 비어있을 때 메시지
            return '💬 Start testing your prompt by typing a message below!';
        },
        isScrollLocked() {
            return this.isNoticeOpen || this.isLoginModalOpen || this.isSignUpModalOpen ||
                this.isAgentModalOpen || this.isMermaidModalOpen || this.isDebugModalOpen ||
                this.isCodeModalOpen || this.isUnitModalOpen;
        }
    },
    mounted() {
        this.fetchChapters();
    }
});

app.mount('#app');
