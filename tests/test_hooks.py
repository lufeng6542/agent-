"""并行审查系统测试"""
import subprocess
import json
import os
import unittest


class TestHookScript(unittest.TestCase):
    """测试 parallel_review_reminder.py"""

    HOOK_PATH = os.path.join(os.path.dirname(__file__), "..", "hooks", "parallel_review_reminder.py")

    def test_script_runs_without_error(self):
        """脚本无报错运行"""
        result = subprocess.run(
            ["python", self.HOOK_PATH],
            capture_output=True, text=True, timeout=10
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

    def test_output_contains_all_phases(self):
        """输出包含三个阶段"""
        result = subprocess.run(
            ["python", self.HOOK_PATH],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout
        self.assertIn("方案评审", output)
        self.assertIn("并行查询", output)
        self.assertIn("完成检查", output)

    def test_output_contains_parallel_agent_count(self):
        """输出提到3个并行Agent"""
        result = subprocess.run(
            ["python", self.HOOK_PATH],
            capture_output=True, text=True, timeout=10
        )
        self.assertIn("3", result.stdout)

    def test_output_contains_exemption_note(self):
        """输出包含豁免说明"""
        result = subprocess.run(
            ["python", self.HOOK_PATH],
            capture_output=True, text=True, timeout=10
        )
        self.assertIn("豁免", result.stdout)


class TestConfigTemplate(unittest.TestCase):
    """测试 settings.template.json"""

    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "settings.template.json")

    def test_valid_json(self):
        """模板是合法JSON"""
        with open(self.TEMPLATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_has_session_start_hook(self):
        """包含 SessionStart hook 配置"""
        with open(self.TEMPLATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("hooks", data)
        self.assertIn("SessionStart", data["hooks"])

    def test_hook_has_placeholder_path(self):
        """hook 命令包含占位符路径"""
        with open(self.TEMPLATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        hooks = data["hooks"]["SessionStart"][0]["hooks"]
        command = hooks[0]["command"]
        self.assertIn("YOUR_HOOKS_PATH", command)


class TestCLAUDEmd(unittest.TestCase):
    """测试 CLAUDE.md"""

    CLAUDE_MD_PATH = os.path.join(os.path.dirname(__file__), "..", "CLAUDE.md")

    def test_file_exists(self):
        """文件存在"""
        self.assertTrue(os.path.exists(self.CLAUDE_MD_PATH))

    def test_contains_all_phases(self):
        """包含三个阶段定义"""
        with open(self.CLAUDE_MD_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("阶段一", content)
        self.assertIn("阶段二", content)
        self.assertIn("阶段三", content)

    def test_contains_exemption_rules(self):
        """包含豁免条件"""
        with open(self.CLAUDE_MD_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("豁免条件", content)

    def test_contains_agent_definitions(self):
        """包含并行Agent定义"""
        with open(self.CLAUDE_MD_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("完整性审查", content)
        self.assertIn("风险评估", content)
        self.assertIn("优化建议", content)


if __name__ == "__main__":
    unittest.main()
