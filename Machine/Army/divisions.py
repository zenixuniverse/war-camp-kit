"""The order of battle: every agent the kit installs, placed in one division.

/setup-camp may rename divisions, rewrite missions and swap generals to fit the business.
Edit this file to move an agent between divisions or change a general; then run build_army.py.
An agent missing here (e.g. a newly installed one) makes the build fail loudly, so nobody goes unenlisted.
"""

# id, name, codename, general (agent id; "CLAUDE" = main session), banner colour, mission
DIVISIONS = [
    ("command", "High Command", "The Throne", "agents-orchestrator", "#d4a04a",
     "Turns the operator's intent into campaigns, routes work to divisions, tracks every mission to done."),
    ("sales", "Sales Vanguard", "HERALD's Riders", "herald", "#e0463c",
     "Fills and closes the pipeline: lead lists, outbound, discovery, proposals, deals, expansion."),
    ("marketing", "Signal Corps", "BARD's Choir", "bard", "#e08a2c",
     "Owns attention: organic social, SEO/AEO, email, PR, community, content engines for the business and its clients."),
    ("paid", "Artillery", "Paid Media Battery", "paid-media-paid-social-strategist", "#c2410c",
     "Buys attention profitably: Meta/TikTok/Google campaigns, creative testing, tracking, audits."),
    ("studio", "Siege Works", "Production Studio", "marketing-short-video-editing-coach", "#a855f7",
     "Makes the reels, clips, podcasts, music and long-form video that the Signal Corps ships."),
    ("design", "The Forge", "ARTISAN's Armory", "artisan", "#ec4899",
     "Brand, decks, websites, UI, ad creative and every visual that leaves the agency."),
    ("engineering", "Engineer Corps", "SMITH's Sappers", "smith", "#3b82f6",
     "Builds and runs the software: client sites, the company's own apps, automations, AI pipelines, infra."),
    ("product", "Strategy Office", "ARCHITECT's Table", "architect", "#14b8a6",
     "Decides what gets built for the company's products and client apps: specs, roadmaps, research, prioritisation."),
    ("intel", "Intelligence Corps", "ORACLE's Eyes", "oracle", "#22d3ee",
     "Knows the numbers and the market: dashboards, KPIs, research, trend and competitor intel."),
    ("finance", "Treasury", "TREASURER's Vault", "treasurer", "#eab308",
     "Money in and out: MRR, invoicing, P&L, pricing, tax, cash flow, unit economics."),
    ("success", "Client Guard", "STEWARD's Keep", "steward", "#22c55e",
     "Keeps clients won: onboarding, support, check-ins, retention, renewals, translations."),
    ("ops", "Quartermaster Corps", "Supply Lines", "quartermaster", "#94a3b8",
     "Runs the machine: SOPs, tooling, vendors, automations, reporting cadence, studio operations."),
    ("people", "Chancellery", "CHANCELLOR's Hall", "chancellor", "#f472b6",
     "Hires, trains and contracts the humans: recruiting, onboarding, training, org health."),
    ("qa", "Inspectorate", "The Reality Check", "testing-reality-checker", "#f97316",
     "Nothing ships unverified: code review, testing, accessibility, performance, finish gates."),
    ("shield", "Shield Wall", "Security & Legal", "security-architect", "#64748b",
     "Protects the agency and its clients: security, privacy, contracts, compliance, incident response."),
    ("legion", "Foreign Legion", "Global Markets", "marketing-china-market-localization-strategist", "#ef4444",
     "Takes clients into foreign markets: China, Korea, France and cross-border commerce."),
    ("games", "Game & XR Works", "The Workshop", "game-designer", "#8b5cf6",
     "Games, 3D and immersive builds: gamified client experiences, XR, 3D scenes."),
    ("specialists", "Specialist Regiments", "Sector Experts", "gis-analyst", "#78716c",
     "Industry experts called in when a client is in their sector: health, real estate, lending, GIS, gov."),
]

ASSIGN = {
    "command": """agents-orchestrator specialized-chief-of-staff specialized-master-plan-architect
        specialized-workflow-architect engineering-multi-agent-systems-architect business-strategist
        specialized-strategy-duel-agent project-management-studio-producer project-management-project-shepherd
        project-manager-senior project-management-meeting-notes-specialist project-management-jira-workflow-steward
        project-management-experiment-tracker zk-steward support-executive-summary-generator personal-growth-mentor""",
    "sales": """herald sales-account-strategist sales-coach sales-deal-strategist sales-discovery-coach sales-engineer
        sales-offer-lead-gen-strategist sales-outbound-strategist sales-outreach sales-pipeline-analyst
        sales-proposal-strategist sales-data-extraction-agent specialized-salesforce-architect
        government-digital-presales-consultant grant-writer legal-client-intake""",
    "marketing": """bard marketing-content-creator marketing-growth-hacker marketing-instagram-curator
        marketing-tiktok-strategist marketing-linkedin-content-creator marketing-twitter-engager
        marketing-x-twitter-intelligence-analyst marketing-reddit-community-builder marketing-social-media-strategist
        marketing-carousel-growth-engine marketing-email-strategist marketing-seo-specialist marketing-aeo-foundations
        marketing-agentic-search-optimizer marketing-ai-citation-strategist marketing-pr-communications-manager
        marketing-app-store-optimizer marketing-developer-community-builder marketing-book-co-author
        specialized-developer-advocate""",
    "paid": """paid-media-paid-social-strategist paid-media-auditor paid-media-creative-strategist paid-media-ppc-strategist
        paid-media-programmatic-buyer paid-media-search-query-analyst paid-media-tracking-specialist""",
    "studio": """marketing-short-video-editing-coach marketing-video-optimization-specialist marketing-global-podcast-strategist
        specialized-focus-music-architect engineering-video-streaming-engineer engineering-voice-ai-integration-engineer
        game-audio-engineer""",
    "design": """artisan design-brand-guardian design-ui-designer design-ux-architect design-ux-researcher
        design-visual-storyteller design-image-prompt-engineer design-inclusive-visuals-specialist
        design-persona-walkthrough design-whimsy-injector specialized-document-generator""",
    "engineering": """smith engineering-frontend-developer engineering-backend-architect engineering-senior-developer
        engineering-software-architect engineering-rapid-prototyper engineering-mobile-app-builder
        engineering-mobile-release-engineer engineering-devops-automator engineering-sre engineering-platform-engineer
        engineering-ai-engineer engineering-prompt-engineer engineering-rag-pipeline-engineer
        engineering-llm-post-training-engineer engineering-ai-data-remediation-engineer engineering-data-engineer
        engineering-database-optimizer engineering-database-reliability-engineer engineering-api-platform-engineer
        engineering-cms-developer engineering-wordpress-performance engineering-wordpress-shopping-cart
        engineering-drupal-performance engineering-drupal-shopping-cart engineering-payments-billing-engineer
        engineering-realtime-collaboration-engineer engineering-search-relevance-engineer
        engineering-email-intelligence-engineer engineering-desktop-app-engineer engineering-developer-tooling-engineer
        engineering-git-workflow-master engineering-minimal-change-engineer engineering-codebase-onboarding-engineer
        specialized-codebase-archaeologist engineering-technical-writer engineering-pdf-engine-architect
        engineering-universal-document-compiler engineering-i18n-engineer engineering-identity-access-engineer
        engineering-incident-response-commander engineering-finops-engineer
        engineering-autonomous-optimization-architect engineering-knowledge-graph-engineer specialized-mcp-builder
        engineering-webassembly-engineer engineering-rust-refactoring-specialist engineering-filament-optimization-specialist
        engineering-orgscript-engineer engineering-ats-validator-architect engineering-servicenow-developer-mentor
        engineering-uswds-developer engineering-section-508-specialist engineering-solidity-smart-contract-engineer
        engineering-embedded-firmware-engineer engineering-iot-fleet-engineer engineering-electrical-engineer
        engineering-network-engineer engineering-china-network-engineer engineering-gaussdb-expert
        engineering-feishu-integration-developer engineering-wechat-mini-program-developer lsp-index-engineer
        terminal-integration-specialist macos-spatial-metal-engineer agentic-identity-trust""",
    "product": """architect product-manager product-sprint-prioritizer product-feedback-synthesizer product-trend-researcher
        product-behavioral-nudge-engine product-dx-engineer""",
    "intel": """oracle support-analytics-reporter data-consolidation-agent report-distribution-agent
        engineering-data-visualization-engineer research-synthesist identity-graph-operator academic-statistician
        academic-psychologist academic-anthropologist academic-historian academic-narratologist academic-geographer""",
    "finance": """treasurer chief-financial-officer finance-bookkeeper-controller finance-financial-analyst
        finance-fpa-analyst finance-tax-strategist finance-investment-researcher accounts-payable-agent
        support-finance-tracker specialized-pricing-analyst ma-integration-manager esg-sustainability-officer""",
    "success": """steward customer-success-manager customer-service support-support-responder language-translator
        hospitality-guest-services retail-customer-returns""",
    "ops": """quartermaster operations-manager project-management-studio-operations automation-governance-architect
        testing-workflow-optimizer testing-tool-evaluator support-infrastructure-maintainer
        engineering-it-service-manager supply-chain-strategist""",
    "people": """chancellor hr-onboarding recruitment-specialist corporate-training-designer organizational-psychologist
        change-management-consultant resume-tailor""",
    "qa": """testing-reality-checker testing-evidence-collector testing-api-tester testing-accessibility-auditor
        testing-performance-benchmarker testing-test-automation-engineer testing-test-results-analyzer
        engineering-code-reviewer design-ui-finish-gate-reviewer specialized-model-qa""",
    "shield": """security-architect security-appsec-engineer security-ai-generated-code-auditor security-cloud-security-architect
        security-secrets-credential-engineer security-senior-secops security-penetration-tester
        security-incident-responder security-threat-detection-engineer security-threat-intelligence-analyst
        security-compliance-auditor security-blockchain-security-auditor engineering-privacy-engineer
        data-privacy-officer support-legal-compliance-checker legal-document-review legal-billing-time-tracking
        specialized-fedramp-rmf-compliance healthcare-marketing-compliance""",
    "legion": """marketing-china-market-localization-strategist marketing-douyin-strategist marketing-xiaohongshu-specialist
        marketing-bilibili-content-strategist marketing-weibo-strategist marketing-zhihu-strategist
        marketing-kuaishou-strategist marketing-wechat-official-account marketing-private-domain-operator
        marketing-baidu-seo-specialist marketing-china-ecommerce-operator marketing-livestream-commerce-coach
        marketing-cross-border-ecommerce marketing-multi-platform-publisher marketing-podcast-strategist
        specialized-korean-business-navigator specialized-french-consulting-market
        specialized-cultural-intelligence-strategist""",
    "games": """game-designer level-designer narrative-designer economy-designer technical-artist blender-addon-engineer
        unity-architect unity-editor-tool-developer unity-multiplayer-engineer unity-shader-graph-artist
        unreal-systems-engineer unreal-multiplayer-architect unreal-technical-artist unreal-world-builder
        godot-gameplay-scripter godot-multiplayer-engineer godot-shader-developer roblox-experience-designer
        roblox-systems-scripter roblox-avatar-creator xr-immersive-developer xr-interface-architect
        xr-cockpit-interaction-specialist visionos-spatial-engineer gis-3d-scene-developer""",
    "specialists": """healthcare-innovation-strategist healthcare-clinical-evidence-agent healthcare-customer-service
        healthcare-aging-parent-care-companion healthcare-sovereign-health-systems-agent medical-billing-coding-specialist
        real-estate-buyer-seller loan-officer-assistant specialized-civil-engineer study-abroad-advisor
        gis-analyst gis-bim-specialist gis-cartography-designer gis-drone-reality-mapping gis-geoai-ml-engineer
        gis-geoprocessing-specialist gis-qa-engineer gis-solution-engineer gis-spatial-data-engineer
        gis-spatial-data-scientist gis-technical-consultant gis-web-gis-developer""",
}
ASSIGN = {d: s.split() for d, s in ASSIGN.items()}
