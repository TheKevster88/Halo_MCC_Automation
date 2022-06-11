from lib2to3.pgen2 import driver
import dearpygui.dearpygui as dpg

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import ElementNotInteractableException,ElementClickInterceptedException,TimeoutException,NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import pyautogui
from os import sys
import getpass
import Settings
import keyboard
import HR_Nightfall_SNIPING_CHALLENGES
import H3ODST_UPLIFT_RESERVE_PLAYTHROUGH
#pip install dearpygui
#pip install pyautogui
#pip install pynput
#pip install opencv-python
#pip install pillow
#pip install 2to3

def main_menu():
	if dpg.does_item_exist("main_menu"):
		dpg.show_item("main_menu")
	else:
		with dpg.window(label="Main Menu",tag="main_menu", width=850,height=500):
			dpg.add_text("Halo MCC challenge automation tool\n\n")
			dpg.add_text("NOTE: MAKE SURE THAT YOU ARE HOVERING OVER CAMPAIGN IN MAIN MENU WHEN STARTING A SCRIPT WITH THE GAME ALREADY OPEN!!!\nGAME MUST BE IN 1600x900 RESOLUTION OR AUTOMATION WILL FAIL")
			dpg.add_button(label="Open Halo MCC")
			dpg.add_text("\n")
			dpg.add_button(label="Challenge Menu",callback=challenges.challenge_menu)
			dpg.add_text("\n")
			dpg.add_button(label="Campaign configurator",callback=Start_campaign.campaign_menu)
			dpg.add_text("\n")
			dpg.add_button(label="Configure game settings (load presets)",callback=settings_configuration)
			dpg.add_text("\n")
			dpg.add_button(label="Return to starting position from main menus",callback=ingame_return_to_starting_place)


def ingame_return_to_starting_place():
	print("this returns to the main starting screen hovering over the campaign button")
	selgui.click(r'Menu_Navigation/Window_Identifier.jpg', .9)
	print("window clicked.")
	time.sleep(1)
	try:
		selgui.hover(r'Start_Campaign/SAVEQUIT.png',.9)
		pyautogui.click()
		time.sleep(1)
		selgui.click(r'Start_Campaign/YES_1.png',.9)
		time.sleep(5)
	except:
		try:
			selgui.hover(r'Start_Campaign/SAVEQUIT.png',.9)
			selgui.click(r'Start_Campaign/SAVEQUIT.png',.9)
			selgui.click(r'Start_Campaign/YES_1.png',.9)
			time.sleep(5)
		except:
			print("save/quit not present, skipping in game exit function...")
	for i in range(15):
		try:
			selgui.hover(r'Menu_Navigation/Main_menu_campaign_unselected.png',.7)
			break
		except:
			keyboard.press_and_release('escape')
			#selgui.press('escape')
			print("escape pressed.")
		time.sleep(1)

	selgui.hover(r'Menu_Navigation/Main_menu_campaign_unselected.png',.7)
	print("task complete.")


class challenges:
	def challenge_menu():
		
		if dpg.does_item_exist("gui_challenge_menu"):
			dpg.show_item("gui_challenge_menu")
			
		else:
			with dpg.window(label="Challenge Menu",tag="gui_challenge_menu", width=500,height=500):
				
				
				dpg.add_button(label="Pull challenges and append to list.",callback=challenges.pull_challenges)
				dpg.add_text("Pulled (automatable) Challenges: ",tag="pulled_challenge_list")
				dpg.add_text("\n\n")
				dpg.add_text("Select challenge")
				dpg.add_listbox(["skulldoggery","From the Beginning...","Playlist Progression","Pinpoint","Eagle Eyed","Car Alarm","Narrative Navigator","Send It"],tag="current_selected_challenge",width=250,callback=challenges.challenge_description_generator)
				dpg.add_button(label="Show challenge description",callback=challenges.challenge_description_window)
				dpg.add_text("\n\n")
				dpg.add_button(label="Execute challenge completion automation",callback=start_challenge.challenge_preset_configurator)
				dpg.add_text("\n\n")
				dpg.add_button(label="Back to Main Menu",callback=main_menu)
				
	def challenge_description_generator():
		current_selected_challenge = dpg.get_value("current_selected_challenge")
		if dpg.does_item_exist("challenge_description"):
			if current_selected_challenge == "skulldoggery":
				dpg.set_value("current_challenge_description","Complete a mission with a skull enabled\n\nAction: H3ODST Uplift Reserve FAMINE")
			elif current_selected_challenge == "From the Beginning...":
				dpg.set_value("current_challenge_description","Complete Missions in CE or Reach\n\nAction: HR NIGHTFALL")
			elif current_selected_challenge == "Playlist Progression":
				dpg.set_value("current_challenge_description","Complete Mission from playlist\n\nAction: H3ODST Vehicle Rally First mission")
			elif current_selected_challenge == "Pinpoint":
				dpg.set_value("current_challenge_description","Kills with precision weapons.\n\nAction: HR Nightfall loop on first elite kill")
			elif current_selected_challenge == "Eagle Eyed":
				dpg.set_value("current_challenge_description","Kills with UNSC weapons.\n\nAction: H3ODST ONI Alpha Site start with spartan laser\n-loop til complete")
			elif current_selected_challenge == "Car Alarm":
				dpg.set_value("current_challenge_description","Kills with Vehicle weapons.\n\nAction: HR Tip of the spear falcon vehicle grenade launcher\n-loop til complete")
			elif current_selected_challenge == "Narrative Navigator":
				dpg.set_value("current_challenge_description","Complete Missions.\n\nAction: H3ODST Uplift Reserve Normal difficulty\n-loop til complete")
			elif current_selected_challenge == "Send It":
				dpg.set_value("current_challenge_description","Defeat enemies with sniping weapons in PvE modes.\n\nAction: HR Nightfall loop on first elite kill")
			else:
				dpg.set_value("current_challenge_description","No known challenge selected.")

	def challenge_description_window():
		
		if dpg.does_item_exist("challenge_description"):
			dpg.show_item("challenge_description")
		else:
			with dpg.window(label="Challenge Description Window",tag="challenge_description",width=550,height=350):
				
				dpg.add_text("",tag="current_challenge_description")
		challenges.challenge_description_generator()
				
	def pull_challenges():
		print("pulling challenges...")
		ingame_return_to_starting_place()
		selgui.click(r'Menu_Navigation/Main_menu_options_and_careers_unselected.png',.7)
		time.sleep(1.5)
		selgui.click(r'Menu_Navigation/Main_menu_challenge_hub_unselected.png',.7)
		time.sleep(1.5)
		pulled_challenge_list = "Pulled (automatable) Challenges:\n"
		dpg.set_value("pulled_challenge_list",pulled_challenge_list)
		challenges.pull_pve_challenges(pulled_challenge_list)
	def update_pulled_challenge_list(pulled_challenge_list):
		dpg.set_value("pulled_challenge_list",pulled_challenge_list)
	def pull_pvp_challenges(pulled_challenge_list):
		#click pvp button at top
		#pvp challenges have 13 challenges
		total_challenges=13
		selgui.click(r'Menu_Navigation/challenge_hub_weekly_pvp.png',.9)
		time.sleep(1.5)
		
		


	def pull_pve_challenges(pulled_challenge_list):
		total_challenges=13
		selgui.click(r'Menu_Navigation/challenge_hub_weekly_pve.png',.9)
		time.sleep(1.5)
		#click pve button at top
		#pve challenges have 13 challenges
		#list of found challenges
		found_Car_Alarm=False
		found_Eagled_Eyed=False
		found_Forza_Firefight=False
		found_From_The_Beginning=False
		found_Narrative_Navigator=False
		found_Pinpoint=False
		found_Playlist_Progression=False
		found_Skulldoggery=False
		found_Send_It=False
		for i in range(4):
			time.sleep(1)
			if found_Car_Alarm==False:
				try:
					print("finding Car Alarm")
					selgui.hover(r'Challenge_Pulling/Car_Alarm.png',.9)
					print("found Car Alarm")
					found_Car_Alarm=True
					pulled_challenge_list= pulled_challenge_list + "\nCar Alarm - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			if found_Narrative_Navigator==False:
				try:
					print("Finding Narrative Navigator")
					selgui.hover(r'Challenge_Pulling/Narrative_Navigator.png',.9)
					print("Found Narrative Navigator")
					found_Narrative_Navigator=True
					pulled_challenge_list = pulled_challenge_list +  "\nNarrative Navigator - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			if found_Forza_Firefight==False:
				try:
					print("finding Forza Firefight")
					selgui.hover(r'Challenge_Pulling/Forza_Firefight.png',.9)
					print("found Forza Firefight")
					found_Forza_Firefight=True
					pulled_challenge_list= pulled_challenge_list + "\nForza Firefight - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			if found_Eagled_Eyed==False:
				try:
					print("finding Eagle Eyed")
					selgui.hover(r'Challenge_Pulling/Eagle_Eyed.png',.9)
					print("found Eagle Eyed")
					found_Eagled_Eyed=True
					pulled_challenge_list= pulled_challenge_list + "\nEagle Eyed - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			if found_Pinpoint==False:
				try:
					print("finding Pinpoint")
					selgui.hover(r'Challenge_Pulling/Pinpoint.png',.9)
					print("found Pinpoint")
					found_Pinpoint=True
					pulled_challenge_list= pulled_challenge_list + "\nPinpoint - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			if found_Skulldoggery==False:
				try:
					print("finding Skulldoggery")
					selgui.hover(r'Challenge_Pulling/Skulldoggery.png',.9)
					print("found Skulldoggery")
					found_Skulldoggery=True
					pulled_challenge_list= pulled_challenge_list + "\nSkulldoggery - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			if found_Playlist_Progression==False:
				try:
					print("finding Playlist Progression")
					selgui.hover(r'Challenge_Pulling/Playlist_Progression.png',.9)
					print("found Playlist Progression")
					found_Playlist_Progression=True
					pulled_challenge_list= pulled_challenge_list + "\nPlaylist Progression - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			if found_From_The_Beginning==False:
				try:
					print("finding From The Beginning")
					selgui.hover(r'Challenge_Pulling/From_The_Beginning.png',.9)
					print("found From The Beginning")
					found_From_The_Beginning=True
					pulled_challenge_list= pulled_challenge_list + "\nFrom The Beginning - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			if found_Send_It==False:
				try:
					print("finding Sent It")
					selgui.hover(r'Challenge_Pulling/Send_It.png',.9)
					print("found Sent IT")
					found_Send_It=True
					pulled_challenge_list= pulled_challenge_list + "\nSend It - PVE"
					print(pulled_challenge_list)
					challenges.update_pulled_challenge_list(pulled_challenge_list)
				except:
					pass
			x, y = pyautogui.locateCenterOnScreen(r'Challenge_Pulling/drag_bar.png', confidence=.9)
			pyautogui.moveTo(x, y)
			time.sleep(.5)
			pyautogui.dragTo(x,y+110,1,button='left')
		return pulled_challenge_list
class start_challenge:
	def challenge_preset_configurator(challenge):
		current_selected_challenge = dpg.get_value("current_selected_challenge")

		#<GAME>(mission_type,mission,rally_point,skulls)
		#Games = Reach,CEA,H2,H3,H3ODST,H4
		#mission_type = mission,playlist
		#mission = campaign name from list in campaign configurator
		#rally_point = alpha,bravo,charlie,delta
		#skulls = none,famine
 
		if current_selected_challenge == "skulldoggery":
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","Complete a mission with a skull enabled \n\nAction: H3ODST Uplift Reserve FAMINE")
			Start_campaign.H3ODST("mission","UPLIFT_RESERVE","alpha","famine")
			H3ODST_UPLIFT_RESERVE_PLAYTHROUGH.play_mission()

		elif current_selected_challenge == "From the Beginning...":
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","Complete Missions in CE or Reach\n\nAction: HR NIGHTFALL")
			Start_campaign.Reach("mission","NIGHTFALL","alpha","none")
			time.sleep(25)
		elif current_selected_challenge == "Pinpoint":
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","Kills with precision weapons.\n\nAction: HR Nightfall loop on first elite kill")
			Start_campaign.Reach("mission","NIGHTFALL","alpha","none")
			time.sleep(25)
			HR_Nightfall_SNIPING_CHALLENGES.play_mission_snipe_100()
		elif current_selected_challenge == "Eagle Eyed":
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","Kills with UNSC weapons.\n\nAction: HR Nightfall loop on first elite kill")
			Start_campaign.Reach("mission","NIGHTFALL","alpha","none")
			time.sleep(25)
			HR_Nightfall_SNIPING_CHALLENGES.play_mission_snipe_100()
		elif current_selected_challenge == "Car Alarm":
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","Kills with Vehicle weapons.\n\nAction: HR Tip of the spear falcon vehicle grenade launcher\n-loop til complete")

		elif current_selected_challenge == "Narrative Navigator":
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","Complete Missions.\n\nAction: H3ODST Uplift Reserve Normal difficulty\n-loop til complete")
			Start_campaign.H3ODST("mission","UPLIFT_RESERVE","alpha","none")
			time.sleep(25)
			H3ODST_UPLIFT_RESERVE_PLAYTHROUGH.play_mission()
		elif current_selected_challenge == "Playlist Progression":
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","Complete Mission from playlist\n\nAction: H3ODST Vehicle Rally First mission")
			Start_campaign.H3ODST("playlist","VEHICLE_RALLY","alpha","none")
			time.sleep(25)
			H3ODST_UPLIFT_RESERVE_PLAYTHROUGH.play_mission()
		elif current_selected_challenge == "Send It":
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","Defeat enemies with sniping weapons in PvE modes.\n\nAction: HR Nightfall loop on first elite kill")
			Start_campaign.Reach("mission","NIGHTFALL","alpha","none")
			time.sleep(25)
			HR_Nightfall_SNIPING_CHALLENGES.play_mission_snipe_75()

		else:
			if dpg.does_item_exist("challenge_description"):
				dpg.set_value("current_challenge_description","No known challenge selected.")


class Start_campaign:
	def campaign_menu():
		if dpg.does_item_exist("campaign_menu"):
			dpg.show_item("campaign_menu")
		else:
			with dpg.window(label="Campaign Menu",tag="campaign_menu", width=500,height=500):
				dpg.add_text("Halo MCC Campaign Configurator Menu\n\n")
				dpg.add_text("Game:")
				dpg.add_listbox(["Halo Reach","Halo Combat Evolved Anniversary","Halo 2","Halo 3","Halo 3 ODST","Halo 4"],tag="Halo_Game")
				dpg.add_text("Mission:")
				dpg.add_listbox(['NIGHTFALL','TIPOFTHESPEAR','UPLIFT_RESERVE','DAWN'],tag="mission")
				dpg.add_text("Rally Point")
				dpg.add_listbox(["alpha","bravo","charlie","delta"],tag="rally_point")
				dpg.add_checkbox(label="Skulls?",tag="skulls")
				dpg.add_text("\n\n")
				dpg.add_button(label="Start Mission",callback=Start_campaign.start_mission_from_menu)
	def start_mission_from_menu():
		ingame_return_to_starting_place()
		game=dpg.get_value("Halo_Game")
		mission_type = 'mission'
		mission = dpg.get_value("mission")
		rally_point = dpg.get_value("rally_point")
		#checks the checkmark for the skulls tag...
		skulls = dpg.get_value("skulls")
		if skulls == True:
			#famine is the only skull that will be coded into automation, due to most of the campaign runs that will be automated 
			#will not involve shooting constantly.
			skulls = 'famine'
		else:
			skulls = 'none'

		#call function based on game selected....
		if game == 'Halo Reach':
			Start_campaign.Reach(mission_type,mission,rally_point,skulls)
		if game == 'Halo Combat Evolved Anniversary':
			Start_campaign.CEA(mission_type,mission,rally_point,skulls)
		if game == 'Halo 2':
			Start_campaign.H2A(mission_type,mission,rally_point,skulls)
		if game == 'Halo 3':
			Start_campaign.H3(mission_type,mission,rally_point,skulls)
		if game == 'Halo 3 ODST':
			Start_campaign.H3ODST(mission_type,mission,rally_point,skulls)
		if game == 'Halo 4':
			Start_campaign.H4(mission_type,mission,rally_point,skulls)

	def click_campaign():
		print("clicking campaign")
		selgui.click(r'Menu_Navigation/Main_menu_campaign_unselected.png',.7)
	def check_mission_type(mission_type):
		print("mission type function")
		if mission_type in ['mission']:
			try:
				selgui.click(r'Start_Campaign/Missions.png',.7)
			except:
				print("was unable to click mission")
		if mission_type in['playlist']:
			try:
				selgui.click(r'Start_Campaign/Playlists.png',.7)
			except:
				print("unable to click playlists")
		time.sleep(2)
	
	def select_mission(mission):
		if mission in ['NIGHTFALL']:
			print(mission + " selected")
			while True:
				try:
					selgui.hover(r'Start_Campaign/NOBLE_ACTUAL.png',.9)
					selgui.click(r'Start_Campaign/NIGHTFALL.png',.9)
					break
				except:
					print("couldn't select mission")
		if mission in ['TIPOFTHESPEAR']:
			print(mission + " selected")
			while True:
				try:
					selgui.click(r'Start_Campaign/TIPOFTHESPEAR.png',.9)
					break
				except:
					print("couldn't select mission")
		if mission in ['UPLIFT_RESERVE']:
			print(mission + " selected")
			while True:
				try:
					selgui.click(r'Start_Campaign/UPLIFT_RESERVE.png',.7)
					break
				except:
					print("couldn't select mission")
		if mission in ['DAWN']:
			print(mission + " selected")
			while True:
				try:
					selgui.click(r'Start_Campaign/DAWN.png',.9)
					break
				except:
					print("couldn't select mission")
		time.sleep(2)
		if mission in ['VEHICLE_RALLY']:
			print(mission + " selected")
			while True:
				try:
					selgui.hover(r'Start_Campaign/LASO.png',.9)
					selgui.click(r'Start_Campaign/VEHICLE_RALLY.png',.9)
					selgui.click(r'Start_Campaign/restart_playlist.png',.9)
					selgui.click(r'Start_Campaign/yes.png',.9)
					break
				except:
					print("couldn't select mission")
	
	def rally_point(rally_point):
		print("rally point function")
		if rally_point in ['alpha']:
			pass
		if rally_point in ['bravo']:
			selgui.hover(r'Start_Campaign/BRAVO.png',.9)
			selgui.click(r'Start_Campaign/BRAVO.png',.9)
			pass
		if rally_point in ['charlie']:
			selgui.hover(r'Start_Campaign/CHARLIE.png',.9)
			selgui.click(r'Start_Campaign/CHARLIE.png',.9)
			pass
		if rally_point in ['delta']:
			selgui.hover(r'Start_Campaign/DELTA.png',.9)
			selgui.click(r'Start_Campaign/DELTA.png',.9)
			pass
		time.sleep(2)
	
	def check_skulls(skulls):
		print("skull check function")
		if skulls in ['none']:
			pass
		if skulls in ['famine']:
			selgui.hover(r'Start_Campaign/Missions_page_hover_bigtext.png',.9)
			selgui.click(r'Start_Campaign/Skulls.png',.9)
			while True:
				try:
					selgui.hover(r'Start_Campaign/Accept_Skulls.png',.9)
					break
				except:
					print("finding accept skulls again...")
			time.sleep(1)
			try:
				print("finding already enabled skull")
				selgui.hover(r'Start_Campaign/Famine_enabled.png',.9)
				print("found famine skull already enabled")
			except:
				print("clicking on famine skull")
				selgui.click(r'Start_Campaign/Famine.png',.9)
			selgui.click(r'Start_Campaign/Accept_Skulls.png',.9)
			pass
		time.sleep(2)

	def start_mission():
		print("starting mission")
		time.sleep(1)
		selgui.hover(r'Start_Campaign/Missions_page_hover_bigtext.png',.7)
		time.sleep(1)
		selgui.click(r'Start_Campaign/start_1.png',.8)
		time.sleep(1)
		try:
			selgui.hover(r'Start_Campaign/warning_progress_lost.png',.8)
			selgui.click(r'Start_Campaign/YES_1.png',.8)
			time.sleep(1)
		except:
			print("did not detect warning popup")
		
		selgui.click(r'Start_Campaign/start_2.png',.9)
		time.sleep(2)
		#logic to check if warning popup for loosing progress appears...
		try:
			selgui.hover(r'Start_Campaign/warning_progress_lost.png',.9)
			selgui.click(r'Start_Campaign/YES_1.png',.9)
		except:
			print("did not detect warning popup")
	def start_playlist_mission():
		print("starting playlist mission")
		time.sleep(1)
		selgui.hover(r'Start_Campaign/Missions_page_hover_bigtext_playlist.png',.9)
		time.sleep(1)
		selgui.click(r'Start_Campaign/start_1.png',.8)
		time.sleep(1)
		try:
			selgui.hover(r'Start_Campaign/warning_progress_lost.png',.8)
			selgui.click(r'Start_Campaign/YES_1.png',.8)
			time.sleep(1)
		except:
			print("did not detect warning popup")
		
		selgui.click(r'Start_Campaign/start_2.png',.9)
		time.sleep(2)
		#logic to check if warning popup for loosing progress appears...
		try:
			selgui.hover(r'Start_Campaign/warning_progress_lost.png',.9)
			selgui.click(r'Start_Campaign/YES_1.png',.9)
		except:
			print("did not detect warning popup")
		



	def Reach(mission_type,mission,rally_point,skulls):
		ingame_return_to_starting_place()
		Start_campaign.click_campaign()
		selgui.click(r'Start_Campaign/Halo_Reach_Campaign.png',.7)
		time.sleep(2)
		Start_campaign.check_mission_type(mission_type)
		time.sleep(2)
		Start_campaign.select_mission(mission)
		Start_campaign.rally_point(rally_point)
		Start_campaign.check_skulls(skulls)
		Start_campaign.start_mission()
		
	def CEA(mission_type,mission,rally_point,skulls):
		ingame_return_to_starting_place()
		Start_campaign.click_campaign()
		selgui.click(r'Start_Campaign/CEA_Campaign.png',.7)
		time.sleep(2)
		Start_campaign.check_mission_type(mission_type)
		time.sleep(2)
		Start_campaign.select_mission(mission)
		Start_campaign.rally_point(rally_point)
		Start_campaign.check_skulls(skulls)
		Start_campaign.start_mission()
	def H2A(mission_type,mission,rally_point,skulls):
		ingame_return_to_starting_place()
		Start_campaign.click_campaign()
		selgui.click(r'Start_Campaign/H2A_Campaign.png',.7)
		time.sleep(2)
		Start_campaign.check_mission_type(mission_type)
		time.sleep(2)
		Start_campaign.select_mission(mission)
		Start_campaign.rally_point(rally_point)
		Start_campaign.check_skulls(skulls)
		Start_campaign.start_mission()
	def H3(mission_type,mission,rally_point,skulls):
		ingame_return_to_starting_place()
		Start_campaign.click_campaign()
		selgui.click(r'Start_Campaign/H3_Campaign.png',.7)
		time.sleep(2)
		Start_campaign.check_mission_type(mission_type)
		time.sleep(2)
		Start_campaign.select_mission(mission)
		Start_campaign.rally_point(rally_point)
		Start_campaign.check_skulls(skulls)
		Start_campaign.start_mission()
	def H3ODST(mission_type,mission,rally_point,skulls):
		ingame_return_to_starting_place()
		Start_campaign.click_campaign()
		selgui.click(r'Start_Campaign/H3ODST_Campaign.png',.7)
		time.sleep(2)
		Start_campaign.check_mission_type(mission_type)
		time.sleep(2)
		Start_campaign.select_mission(mission)
		if mission_type == "mission":
			Start_campaign.rally_point(rally_point)
			Start_campaign.check_skulls(skulls)
			Start_campaign.start_mission()
		else:
			Start_campaign.start_playlist_mission()
	def H4(mission_type,mission,rally_point,skulls):
		ingame_return_to_starting_place()
		Start_campaign.click_campaign()
		selgui.click(r'Start_Campaign/H4_Campaign.png',.9)
		time.sleep(2)
		Start_campaign.check_mission_type(mission_type)
		time.sleep(2)
		Start_campaign.select_mission(mission)
		Start_campaign.rally_point(rally_point)
		Start_campaign.check_skulls(skulls)
		Start_campaign.start_mission()
def settings_configuration():
	print("settings configuration menu")
	ingame_return_to_starting_place()
	selgui.click(r'Menu_Navigation/Main_menu_options_and_careers_unselected.png',.7)
	selgui.click(r'Menu_Navigation/Settings.png',.7)
	selgui.click(r'Menu_Navigation/configure_mousekeyboard.png',.7)
	selgui.click(r'Menu_Navigation/mouse_sensitivity_box.png',.9)
	time.sleep(3)
	selgui.click(r'Menu_Navigation/mouse_sensitivity_box_2.png',.9)
	print("Sensitivity is "+Settings.mouse_sensitivity)
	selgui.write('none',Settings.mouse_sensitivity,.7)
	selgui.click(r'Menu_Navigation/Back.png',.7)
	time.sleep(1)
	selgui.click(r'Menu_Navigation/Back.png',.7)
	time.sleep(1)
	try:
		selgui.hover(r'Menu_Navigation/Save_Settings.png',.7)
		selgui.click(r'Menu_Navigation/Save_Settings.png',.7)
	except:
		pass
class sys:

	def press_enter():
		input("Press enter to continue...")
class selgui:
	def hover(element,confidence_value):
		x, y = pyautogui.locateCenterOnScreen(element, confidence=confidence_value)
		pyautogui.moveTo(x, y)
	def click(element,confidence_value):
		while True:
			try:
				x, y = pyautogui.locateCenterOnScreen(element, confidence=confidence_value)
				break
			except:
				print("trying again")
		pyautogui.moveTo(x, y, .25)
		pyautogui.click()

	def write(element,data,confidence_value):
		if element in ['none']:
			pyautogui.write(data)
			#this is mainly if the mouse is already in the location you need and just want to type, if an element 'image to find' is specified, it will first click and then type
		else:
			x, y = pyautogui.locateCenterOnScreen(element, confidence=confidence_value)
			pyautogui.moveTo(x, y, .25)
			pyautogui.click()
			pyautogui.write(data)
				
		
	def press(data):
		pyautogui.press(data)
		#['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
		#')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
		#'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
		#'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
		#'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
		#'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
		#'browserback', 'browserfavorites', 'browserforward', 'browserhome',
		#'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
		#'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
		#'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
		#'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
		#'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
		#'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
		#'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
		#'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
		#'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
		#'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
		#'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
		#'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
		#'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
		#'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
		#'command', 'option', 'optionleft', 'optionright']
class processes:
    def start_MCC():
        print('hi')


dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()






main_menu()






#this goes at the very end of the script
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

