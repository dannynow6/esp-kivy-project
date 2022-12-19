# File name: main.py

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

import config
import random

""" 
A simple Kivy App that uses buzzsprout api to get episode data for my podcast - ESP
- use this info to display important stats, milestone, and episode info 
- app includes access to podcast webpage, YouTube, etc. 
"""


class EspApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "LightBlue"
        self.theme_cls.material_style = "M3"

        return Builder.load_file("esp_1.kv")

    def esp_data_report(self):
        # Make Buzzsprout API request and get episode info
        # Return info as key, value pairs (json) and attach to episodes variable
        episodes = config.get_esp_info()
        total_ep = len(episodes)
        num_eps = str(total_ep)
        listens = [episode["total_plays"] for episode in episodes]
        plays = str(sum(listens))
        current_ep = episodes[0]
        recent_ep = current_ep["episode_number"]
        current_season = current_ep["season_number"]
        ep_duration = current_ep["duration"] / 60
        ep_dur_format = format(ep_duration, ".2f")
        ep_title = current_ep["title"]
        ep_plays = current_ep["total_plays"]

        self.root.ids.tot_eps.text = f"Total Esp Episodes: {num_eps}\nTotal Listens: {plays}\n\nMost Recent Episode: {ep_title}, S0{current_season}.ep{recent_ep}\nDuration: {ep_dur_format}\nPlays: {ep_plays}"

    def top_episodes(self):
        episodes = config.get_esp_info()
        z = 200
        top_name = [
            episode["title"] for episode in episodes if episode["total_plays"] > z
        ]
        top_num = [
            episode["episode_number"]
            for episode in episodes
            if episode["total_plays"] > z
        ]
        i = 0
        for ep in top_name:
            self.root.ids.top_ep.add_widget(
                MDLabel(text=f"{i + 1}. {ep}, ep #{top_num[i]}", halign="center")
            )
            i += 1

    def recommended_eps(self):
        episodes = config.get_esp_info()
        ep_names = [episode["title"] for episode in episodes]
        ep_num = [episode["episode_number"] for episode in episodes]
        x = random.randint(1, (len(ep_names) + 1))
        self.root.ids.rec_eps.add_widget(
            MDLabel(text=f"{ep_names[x]}, #{ep_num[x]}", halign="center")
        )


if __name__ == "__main__":
    EspApp().run()
