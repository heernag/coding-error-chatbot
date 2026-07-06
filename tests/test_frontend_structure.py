from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


class FrontendStructureTest(unittest.TestCase):
    def test_vite_react_typescript_files_exist(self):
        expected_files = [
            FRONTEND / "package.json",
            FRONTEND / "index.html",
            FRONTEND / "vite.config.ts",
            FRONTEND / "tsconfig.json",
            FRONTEND / "tsconfig.app.json",
            FRONTEND / "tsconfig.node.json",
            FRONTEND / "src" / "main.tsx",
            FRONTEND / "src" / "App.tsx",
            FRONTEND / "src" / "App.css",
            FRONTEND / "src" / "index.css",
            FRONTEND / "README.md",
        ]

        for file_path in expected_files:
            self.assertTrue(file_path.exists(), f"{file_path} should exist")

    def test_app_connects_to_chat_api_and_filters_diagnosis_card(self):
        app = (FRONTEND / "src" / "App.tsx").read_text(encoding="utf-8")

        self.assertIn("/api/chat", app)
        self.assertIn("session_id", app)
        self.assertIn("parseAnswerSections", app)
        self.assertIn("[오류 요약]", app)
        self.assertIn("[주의사항]", app)
        self.assertIn("type ChatMessage", app)
        self.assertIn('section.title !== "[진단 방법]"', app)

    def test_enter_key_submits_without_newline(self):
        app = (FRONTEND / "src" / "App.tsx").read_text(encoding="utf-8")

        self.assertIn("handleComposerKeyDown", app)
        self.assertIn("event.key === \"Enter\"", app)
        self.assertIn("!event.shiftKey", app)
        self.assertIn("event.preventDefault()", app)
        self.assertIn("onKeyDown={handleComposerKeyDown}", app)

    def test_answer_cards_show_titles_without_header_subtitle_or_arrow(self):
        app = (FRONTEND / "src" / "App.tsx").read_text(encoding="utf-8")

        self.assertNotIn("Vite + React + TypeScript", app)
        self.assertIn("<h2>{section.title}</h2>", app)
        self.assertNotIn(">↑</button>", app)

    def test_styles_define_reversed_messenger_layout(self):
        css = (FRONTEND / "src" / "App.css").read_text(encoding="utf-8")

        self.assertIn(".message.user", css)
        self.assertIn(".message.bot", css)
        self.assertIn(".answer-section", css)
        self.assertIn("max-width: 760px", css)
        self.assertIn(".message.bot {\n  flex-direction: row-reverse;", css)
        self.assertIn(".message.user {\n  flex-direction: row;", css)

    def test_answer_section_titles_are_prominent(self):
        css = (FRONTEND / "src" / "App.css").read_text(encoding="utf-8")

        self.assertIn(".answer-section h2", css)
        self.assertIn("font-size: 16px", css)
        self.assertIn("font-weight: 800", css)

    def test_answer_sections_use_dividers_instead_of_inner_cards(self):
        css = (FRONTEND / "src" / "App.css").read_text(encoding="utf-8")

        self.assertIn(".answer-section + .answer-section", css)
        self.assertIn("border-top: 1px dashed", css)
        self.assertNotIn(".answer-section {\n  padding: 10px 12px;\n  background:", css)
        self.assertNotIn(".answer-section {\n  padding: 10px 12px;\n  border:", css)

    def test_boilerplate_removes_unused_vite_assets(self):
        removed_files = [
            FRONTEND / "src" / "assets" / "react.svg",
            FRONTEND / "public" / "vite.svg",
        ]

        for file_path in removed_files:
            self.assertFalse(file_path.exists(), f"{file_path} should be removed")

    def test_readme_explains_install_and_dev(self):
        readme = (FRONTEND / "README.md").read_text(encoding="utf-8")

        self.assertIn("npm install", readme)
        self.assertIn("npm run dev", readme)
        self.assertIn("Vite", readme)
        self.assertIn("React", readme)
        self.assertIn("TypeScript", readme)


if __name__ == "__main__":
    unittest.main()
