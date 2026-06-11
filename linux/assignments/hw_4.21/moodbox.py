
"""
情绪反馈盒子 - 互动式控制台游戏
带有成就系统、时间限制和非线性情绪变化
"""

import sys
import time
import tty
import termios
import select
import os
import math
import random

class SentientBoxV2:
    def __init__(self):
        # 游戏状态
        self.max_patience = 100
        self.patience = 100.0
        self.suspicion = 0.0
        self.last_update = time.time()
        
        # 界面显示
        self.msg = "他在盒子里打瞌睡..."
        self.is_on = False
        
        # 游戏统计
        self.probe_count = 0
        self.flip_count = 0
        self.game_over = False
        self.victory = False
        self.start_time = time.time()
        
        # 成就系统
        self.achievements = {
            'stealth': {'name': '幽灵玩家', 'unlocked': False, 'desc': '全程警觉度不超过30'},
            'masochist': {'name': '受虐狂', 'unlocked': False, 'desc': '连续试探10次不拨开关'},
            'speed_demon': {'name': '闪电侠', 'unlocked': False, 'desc': '30秒内拨开开关5次'},
            'patient_master': {'name': '耐心大师', 'unlocked': False, 'desc': '拨开开关15次不Game Over'},
            'curious_george': {'name': '好奇宝宝', 'unlocked': False, 'desc': '触发所有警觉度对话'},
            'speed_runner': {'name': '速通玩家', 'unlocked': False, 'desc': '2分钟内让盒子生气'},
            'zen_master': {'name': '禅意大师', 'unlocked': False, 'desc': '保持耐心值>90超过1分钟'},
            'chaos_agent': {'name': '混沌使者', 'unlocked': False, 'desc': '同时让耐心<20且警觉>80'},
            'perfectionist': {'name': '完美主义者', 'unlocked': False, 'desc': '不触发任何生气警告完成游戏'},
            'social_butterfly': {'name': '社交达人', 'unlocked': False, 'desc': '试探和拨开次数相等且都>5'}
        }
        
        # 警觉度对话记录
        self.suspicion_messages = set()
        self.last_probe_time = 0
        self.consecutive_probes = 0
        self.last_flip_time = 0
        self.flip_times = []
        
        # 检测运行环境
        self.in_vim = self.check_vim_environment()
    
    def check_vim_environment(self):
        """检测是否在Vim中运行"""
        vim_indicators = [
            'VIM' in os.environ.get('TERM', ''),
            'vim' in os.environ.get('VIM', ''),
            os.environ.get('VIMRUNTIME') is not None,
        ]
        return any(vim_indicators)
    
    def get_input(self, timeout=0.05):
        """获取键盘输入"""
        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                r, _, _ = select.select([sys.stdin], [], [], timeout)
                if r:
                    ch = sys.stdin.read(1)
                    return ch
                return None
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except:
            return None
    
    def nonlinear_patience_recovery(self, current_patience, suspicion):
        """非线性耐心值恢复"""
        # 基础恢复率（正弦波动）
        time_factor = (math.sin(time.time() * 0.5) + 1) / 2  # 0-1之间波动
        base_recovery = 0.15 + time_factor * 0.2
        
        # 警觉度影响（指数衰减）
        suspicion_penalty = math.exp(-suspicion / 30)  # 警觉度越高恢复越慢
        
        # 耐心值本身的影响（曲线）
        if current_patience > 80:
            patience_factor = 0.5  # 高耐心时恢复慢
        elif current_patience < 20:
            patience_factor = 1.5  # 低耐心时恢复快（求生欲）
        else:
            patience_factor = 1.0
        
        # 随机波动
        random_factor = 0.8 + random.random() * 0.4
        
        recovery = base_recovery * suspicion_penalty * patience_factor * random_factor
        return min(recovery, 0.8)  # 最大恢复速度限制
    
    def nonlinear_suspicion_decay(self, current_suspicion):
        """非线性警觉度下降"""
        if current_suspicion > 70:
            decay = 0.3  # 高度警觉时下降慢
        elif current_suspicion > 40:
            decay = 0.6  # 中度警觉
        else:
            decay = 1.0  # 低警觉时快速恢复
        
        # 随机波动
        random_factor = 0.9 + random.random() * 0.2
        return decay * random_factor * 0.5
    
    def update_stats(self):
        """更新耐心值和警觉度（非线性）"""
        now = time.time()
        dt = min(now - self.last_update, 0.5)
        self.last_update = now
        
        # 非线性耐心值恢复
        if self.patience < self.max_patience and not self.is_on:
            recovery = self.nonlinear_patience_recovery(self.patience, self.suspicion)
            self.patience = min(self.max_patience, self.patience + recovery * dt)
        
        # 非线性警觉度下降
        if self.suspicion > 0:
            decay = self.nonlinear_suspicion_decay(self.suspicion)
            self.suspicion = max(0, self.suspicion - decay * dt)
        
        # 检查成就
        self.check_achievements()
    
    def check_achievements(self):
        """检查成就解锁"""
        # 幽灵玩家：全程警觉度不超过30
        if not self.achievements['stealth']['unlocked'] and self.suspicion <= 30:
            if self.flip_count >= 3:  # 至少拨开3次
                self.unlock_achievement('stealth')
        
        # 受虐狂：连续试探10次不拨开关
        if not self.achievements['masochist']['unlocked'] and self.consecutive_probes >= 10:
            self.unlock_achievement('masochist')
        
        # 闪电侠：30秒内拨开开关5次
        if not self.achievements['speed_demon']['unlocked'] and len(self.flip_times) >= 5:
            recent_flips = [t for t in self.flip_times if time.time() - t <= 30]
            if len(recent_flips) >= 5:
                self.unlock_achievement('speed_demon')
        
        # 耐心大师：拨开开关15次不Game Over
        if not self.achievements['patient_master']['unlocked'] and self.flip_count >= 15:
            self.unlock_achievement('patient_master')
        
        # 好奇宝宝：触发所有警觉度对话
        if not self.achievements['curious_george']['unlocked'] and len(self.suspicion_messages) >= 6:
            self.unlock_achievement('curious_george')
        
        # 速通玩家：2分钟内让盒子生气
        if not self.achievements['speed_runner']['unlocked'] and self.game_over:
            elapsed = time.time() - self.start_time
            if elapsed <= 120:
                self.unlock_achievement('speed_runner')
        
        # 禅意大师：保持耐心值>90超过1分钟
        if not self.achievements['zen_master']['unlocked']:
            if hasattr(self, 'zen_start_time') and self.patience > 90:
                if time.time() - self.zen_start_time >= 60:
                    self.unlock_achievement('zen_master')
            elif self.patience > 90:
                self.zen_start_time = time.time()
            else:
                self.zen_start_time = None
        
        # 混沌使者：同时让耐心<20且警觉>80
        if not self.achievements['chaos_agent']['unlocked'] and self.patience < 20 and self.suspicion > 80:
            self.unlock_achievement('chaos_agent')
        
        # 完美主义者：不触发任何生气警告完成游戏
        if not self.achievements['perfectionist']['unlocked'] and self.victory:
            if not hasattr(self, 'anger_warning_triggered') or not self.anger_warning_triggered:
                self.unlock_achievement('perfectionist')
        
        # 社交达人：试探和拨开次数相等且都>5
        if not self.achievements['social_butterfly']['unlocked'] and self.probe_count > 5 and self.flip_count > 5:
            if self.probe_count == self.flip_count:
                self.unlock_achievement('social_butterfly')
    
    def unlock_achievement(self, key):
        """解锁成就"""
        if not self.achievements[key]['unlocked']:
            self.achievements[key]['unlocked'] = True
            self.render()
            print(f"\n🎉 成就解锁：{self.achievements[key]['name']} - {self.achievements[key]['desc']}")
            time.sleep(2)
    
    def render(self):
        """渲染界面"""
        if self.in_vim:
            self.render_vim()
        else:
            self.render_ansi()
    
    def render_ansi(self):
        """ANSI终端渲染（正常模式）"""
        sys.stdout.write("\033[K")
        
        # 非线性状态显示
        p_bar = self.get_nonlinear_bar(self.patience, self.max_patience)
        s_bar = self.get_nonlinear_bar(self.suspicion, 100, is_suspicion=True)
        
        # 情绪状态描述
        emotion = self.get_emotion_state()
        
        # 时间显示
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        print(f"耐心值 [{p_bar}] {self.patience:.1f}/100  |  警觉度 {s_bar} {self.suspicion:.1f}")
        print(f"情绪: {emotion}  |  时间: {minutes:02d}:{seconds:02d}")
        
        box_ui = "  [🔛  ON  ]  " if self.is_on else "  [🔘 OFF ]  "
        sys.stdout.write("\033[K")
        sys.stdout.write(f"{box_ui} {self.msg}\r")
        sys.stdout.write("\033[2A")
        sys.stdout.flush()
    
    def get_nonlinear_bar(self, value, max_val, is_suspicion=False):
        """非线性进度条显示"""
        if is_suspicion:
            # 警觉度的非线性显示（低警觉敏感，高警觉夸张）
            if value < 30:
                display_value = int(value / 3)  # 0-10
            elif value < 70:
                display_value = 10 + int((value - 30) / 4)  # 10-20
            else:
                display_value = 20 + int((value - 70) / 1.5)  # 20-40
            display_value = min(display_value, 40)
        else:
            # 耐心值的非线性显示
            if value > 80:
                display_value = 20 + int((value - 80) / 2)  # 20-30
            elif value > 50:
                display_value = 10 + int((value - 50) / 3)  # 10-20
            else:
                display_value = int(value / 5)  # 0-10
        
        display_value = max(0, min(display_value, 40))
        
        if is_suspicion:
            bar = "⚠️" * display_value
        else:
            bar = "❤️" * display_value
        
        return bar.ljust(40, "░")
    
    def get_emotion_state(self):
        """根据状态返回情绪描述"""
        if self.patience > 80 and self.suspicion < 20:
            return "😊 平静愉快"
        elif self.patience > 60 and self.suspicion < 40:
            return "😐 昏昏欲睡"
        elif self.patience > 40 and self.suspicion < 60:
            return "😕 有点烦躁"
        elif self.patience > 20 and self.suspicion < 80:
            return "😠 不耐烦"
        elif self.patience <= 20 and self.suspicion < 80:
            return "😤 快要爆发"
        elif self.suspicion >= 80:
            return "😨 极度警惕"
        else:
            return "🤔 难以捉摸"
    
    def render_vim(self):
        """Vim兼容渲染"""
        sys.stdout.write("\n" * 4)
        
        p_bar = self.get_nonlinear_bar(self.patience, self.max_patience)
        s_bar = self.get_nonlinear_bar(self.suspicion, 100, is_suspicion=True)
        emotion = self.get_emotion_state()
        
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        print(f"Patience [{p_bar}] {self.patience:.1f}/100  |  Alert {s_bar} {self.suspicion:.1f}")
        print(f"Mood: {emotion}  |  Time: {minutes:02d}:{seconds:02d}")
        
        box_ui = "  [ ON  ]  " if self.is_on else "  [ OFF ]  "
        print(f"{box_ui} {self.msg}")
        print("-" * 60)
        
        sys.stdout.flush()
    
    def action_flip(self):
        """拨开开关（双击空格）"""
        if self.game_over or self.victory:
            return
        
        # 记录拨开时间
        self.flip_times.append(time.time())
        self.flip_times = [t for t in self.flip_times if time.time() - t <= 60]
        
        self.is_on = True
        self.consecutive_probes = 0  # 重置连续试探计数
        
        # 非线性耐心消耗
        if self.patience > 80:
            cost = 5 + random.randint(-2, 2)
            self.msg = random.choice([
                "(┛ಠД尺)┛ < 别动这个开关！",
                "(╬◣д◢) < 你 找 茬 是 吧 ？",
                "(>_<) < 住手！"
            ])
        elif self.patience > 50:
            cost = 10 + random.randint(-3, 3)
            self.msg = random.choice([
                "(；一_一) < 别这样...",
                "(-_-;) < 够了够了",
                "(╯°□°)╯ < 还来？"
            ])
        elif self.patience > 20:
            cost = 20 + random.randint(-5, 5)
            self.msg = random.choice([
                "(҂◡_◡) < 我 生 气 了！",
                "(◣_◢) < 最后警告！",
                "(╬ Ò﹏Ó) < 真的会坏掉！"
            ])
        else:
            cost = 30 + random.randint(-10, 10)
            self.msg = random.choice([
                "(╥﹏╥) < 好痛...",
                "(T_T) < 你欺负人",
                "(;´༎ຶД༎ຶ`) < 住手！"
            ])
        
        # 警觉度影响消耗
        suspicion_multiplier = 1 + (self.suspicion / 100)
        actual_cost = cost * suspicion_multiplier
        
        self.patience -= actual_cost
        self.flip_count += 1
        
        self.render()
        time.sleep(0.6)
        
        self.is_on = False
        
        # 检查游戏结束或胜利
        if self.patience <= 0:
            self.game_over = True
            self.msg = "(╥﹏╥) < 我被你玩坏了..."
        elif self.flip_count >= 15:
            self.victory = True
            self.msg = "(✪▽✪) < 恭喜你获得我的信任！"
        else:
            self.msg = self.get_random_recovery_message()
    
    def action_probe(self):
        """试探盒子（单击空格）"""
        if self.game_over or self.victory:
            return
        
        self.probe_count += 1
        self.consecutive_probes += 1
        self.last_probe_time = time.time()
        
        # 非线性警觉度增加
        base_increase = 5 + random.randint(-2, 8)
        
        # 连续试探加成
        consecutive_bonus = min(self.consecutive_probes * 1.5, 20)
        
        # 当前耐心值影响（低耐心时更敏感）
        patience_factor = 2 if self.patience < 30 else 1
        
        actual_increase = (base_increase + consecutive_bonus) * patience_factor
        self.suspicion = min(100, self.suspicion + actual_increase)
        
        # 记录警觉度对话
        if self.suspicion < 20:
            msg = "(._.) 呼...幻觉吗？"
            self.suspicion_messages.add('low')
        elif self.suspicion < 40:
            msg = "( -_-)? 好像有动静..."
            self.suspicion_messages.add('medium_low')
        elif self.suspicion < 60:
            msg = "(・・?) 什么声音？"
            self.suspicion_messages.add('medium')
        elif self.suspicion < 80:
            msg = "(⊙_⊙) 谁在那？！"
            self.suspicion_messages.add('medium_high')
        else:
            msg = "(◣_◢) 出来！我看到你了！"
            self.suspicion_messages.add('high')
        
        # 记录生气警告
        if self.suspicion > 70 and self.patience < 30:
            self.anger_warning_triggered = True
        
        self.msg = msg
        
        # 随机额外效果
        if random.random() < 0.1:
            self.msg += " (盒子抖了一下)"
    
    def get_random_recovery_message(self):
        """随机恢复消息"""
        messages = [
            "(-_- ) 呼...",
            "(._.) 继续睡觉...",
            "(=^･ω･^=) 喵...",
            "(￣ω￣) 好舒服...",
            "(。-ω-)zzz"
        ]
        return random.choice(messages)
    
    def show_achievements(self):
        """显示成就列表"""
        print("\n" + "=" * 60)
        print("🏆 成就系统 🏆")
        print("=" * 60)
        
        unlocked_count = sum(1 for a in self.achievements.values() if a['unlocked'])
        
        for key, achievement in self.achievements.items():
            status = "✅" if achievement['unlocked'] else "❌"
            print(f"{status} {achievement['name']:15} - {achievement['desc']}")
        
        print("=" * 60)
        print(f"已解锁: {unlocked_count}/{len(self.achievements)}")
        print("=" * 60)
    
    def show_help(self):
        """显示帮助信息"""
        if self.in_vim:
            print("\n操作说明:")
            print("  [空格] - 试探盒子")
            print("  [双击空格] - 拨开开关")
            print("  [A] - 显示成就")
            print("  [H] - 显示帮助")
            print("  [Q] - 退出游戏")
        else:
            print("\n🎮 操作说明:")
            print("  [空格]      - 试探盒子（增加警觉度）")
            print("  [双击空格]  - 拨开开关（消耗耐心值）")
            print("  [A]         - 查看成就")
            print("  [H]         - 显示帮助")
            print("  [Q]         - 退出游戏")
            print("\n💡 游戏机制:")
            print("  • 非线性恢复：耐心值恢复速度受多种因素影响")
            print("  • 连续试探：会增加额外的警觉度")
            print("  • 情绪系统：根据状态显示不同表情")
            print("  • 时间限制：部分成就有时间要求")
    
    def start(self):
        """启动游戏主循环"""
        # 清屏并显示标题
        if not self.in_vim:
            os.system('clear' if os.name == 'posix' else 'cls')
        
        print("╔══════════════════════════════════════════════╗")
        print("║     🎁 情绪反馈盒子 v3.0 🎁                 ║")
        print("║   非线性情绪系统 + 成就系统 + 时间挑战     ║")
        print("╚══════════════════════════════════════════════╝")
        
        if self.in_vim:
            print("\n[Vim兼容模式]")
        
        self.show_help()
        print("\n" + "=" * 60)
        
        # 预留显示区域
        print("\n" * 6)
        
        try:
            while not self.game_over and not self.victory:
                self.update_stats()
                self.render()
                
                key = self.get_input(0.1)
                
                if key:
                    if key.lower() == 'q':
                        print("\n\n👋 游戏已退出！")
                        self.show_achievements()
                        self.show_stats()
                        break
                    elif key.lower() == 'h':
                        self.show_help()
                        time.sleep(2)
                    elif key.lower() == 'a':
                        self.show_achievements()
                        time.sleep(3)
                    elif key == ' ':
                        # 检测双击
                        second_key = self.get_input(0.3)
                        if second_key == ' ':
                            self.action_flip()
                        else:
                            self.action_probe()
                
                # 游戏结束检测
                if self.patience <= 0:
                    self.game_over = True
                    break
                elif self.flip_count >= 15:
                    self.victory = True
                    break
                    
        except KeyboardInterrupt:
            print("\n\n👋 游戏被中断！")
            self.show_stats()
        
        # 游戏结束画面
        if self.game_over:
            print("\n" + "=" * 60)
            print("💀 GAME OVER 💀")
            print("=" * 60)
            self.msg = "(╥﹏╥) < 我被你玩坏了..."
            self.render()
            time.sleep(1)
        elif self.victory:
            print("\n" + "=" * 60)
            print("🎉 胜利！🎉")
            print("=" * 60)
            print("你成功获得了盒子小人的信任！")
            print("他决定从盒子里出来和你做朋友！")
            time.sleep(2)
        
        self.show_stats()
        self.show_achievements()
    
    def show_stats(self):
        """显示游戏统计"""
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        print("\n📊 游戏统计:")
        print(f"  🔍 试探次数: {self.probe_count}")
        print(f"  👐 拨开次数: {self.flip_count}")
        print(f"  💚 最终耐心: {max(0, self.patience):.1f}")
        print(f"  ⚠️  最高警觉: {self.suspicion:.1f}")
        print(f"  ⏱️  游戏时间: {minutes:02d}:{seconds:02d}")
        
        # 计算效率评分
        if self.flip_count > 0:
            efficiency = (self.flip_count / self.probe_count) if self.probe_count > 0 else self.flip_count
            print(f"  📈 效率评分: {efficiency:.2f} (拨开/试探)")

if __name__ == "__main__":
    # 设置环境编码
    if sys.stdout.encoding != 'UTF-8' and hasattr(sys.stdout, 'buffer'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 启动游戏
    game = SentientBoxV2()
    game.start()