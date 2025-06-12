# 使用Kivy重写的UI界面
import os
import random
import time
import pygame
from threading import Thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

# 设置窗口大小和标题
Window.size = (400, 200)

class AudioAppKivy(App):
    def build(self):
        # 初始化Pygame音频
        pygame.mixer.init()
        self.is_playing = False
        self.playback_thread = None

        # 加载音频资源
        self._load_audio_resources()

        # 创建主布局
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # 创建开始按钮
        self.start_btn = Button(
            text='开始模拟',
            size_hint=(1, 0.5),
            font_size=24,
            background_color=(0.2, 0.6, 0.2, 1),  # 绿色
            font_name='SimHei'
        )
        self.start_btn.bind(on_press=self.start_playback)

        # 创建停止按钮
        self.stop_btn = Button(
            text='停止模拟',
            size_hint=(1, 0.5),
            font_size=24,
            background_color=(0.6, 0.2, 0.2, 1),  # 红色
            disabled=True,
            font_name='SimHei'
        )
        self.stop_btn.bind(on_press=self._safe_stop)

        # 添加按钮到布局
        self.layout.add_widget(self.start_btn)
        self.layout.add_widget(self.stop_btn)

        return self.layout

    def start_playback(self, instance):
        if self.is_playing or (self.playback_thread and self.playback_thread.is_alive()):
            return

        # 重置音频系统
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.mixer.init()

        self.is_playing = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False

        # 启动播放线程
        self.playback_thread = Thread(target=self._playback_sequence)
        self.playback_thread.daemon = True
        self.playback_thread.start()

    def _playback_sequence(self):
        try:
            if not self.is_playing:
                return

            # 播放开始音频
            if self.start_audio:
                self.start_audio.play()
                while pygame.mixer.get_busy() and self.is_playing:
                    pygame.time.Clock().tick(10)

            if not self.is_playing:
                return

            # 添加1秒延迟
            current_time = time.strftime("%H:%M:%S")
            delay_log = f'[{current_time}] ##### 添加1秒延迟开始 #####\n'
            with open('delay_verification.log', 'a', encoding='utf-8') as f:
                f.write(delay_log)
            pygame.time.wait(1000)
            current_time = time.strftime("%H:%M:%S")
            delay_log = f'[{current_time}] ##### 1秒延迟结束 #####\n'
            with open('delay_verification.log', 'a', encoding='utf-8') as f:
                f.write(delay_log)

            # 播放指令音频序列
            self._play_audio_sequence()

        except Exception as e:
            print('播放序列异常:', str(e))
        finally:
            if self.is_playing:
                Clock.schedule_once(self._reset_ui, 0)
                self.is_playing = False

    def _play_audio_sequence(self):
        try:
            # 随机选择5条指令播放
            if len(self.instructions) > 5:
                selected_instructions = random.sample(self.instructions, 5)
            else:
                selected_instructions = self.instructions

            for idx, sound in enumerate(selected_instructions, 1):
                if not self.is_playing or sound is None:
                    continue
                sound.play()
                while pygame.mixer.get_busy() and self.is_playing:
                    pygame.time.Clock().tick(10)
                if not self.is_playing:
                    break
                # 指令间增加5秒延迟
                pygame.time.wait(5000)

            # 播放结束音频
            if self.is_playing and self.end_audio:
                self.end_audio.play()
                while pygame.mixer.get_busy() and self.is_playing:
                    pygame.time.Clock().tick(10)

        except Exception as e:
            print('播放异常:', str(e))
        finally:
            Clock.schedule_once(self._reset_ui, 0)

    def _safe_stop(self, instance):
        self.is_playing = False
        pygame.mixer.stop()
        if self.playback_thread and self.playback_thread.is_alive():
            self.playback_thread.join(timeout=1.0)
        pygame.mixer.quit()
        pygame.mixer.init()
        self._reset_ui()
        self._load_audio_resources()

    def _reset_ui(self, dt=None):
        self.start_btn.disabled = False
        self.stop_btn.disabled = True

    def _load_audio_resources(self):
        self.start_audio = self._load_safe('开始语/开始.mp3')
        self.end_audio = self._load_safe('结束语/结束.mp3')
        self.instructions = [self._load_safe(f'指令/{i}.mp3') for i in range(1, 12)]

    def _load_safe(self, file_path):
        try:
            if not os.path.exists(file_path):
                print(f'错误: 文件不存在 - {os.path.abspath(file_path)}')
                return None
            return pygame.mixer.Sound(file_path)
        except Exception as e:
            print(f'音频加载失败: {str(e)} - {file_path}')
            return None

if __name__ == '__main__':
    AudioAppKivy().run()