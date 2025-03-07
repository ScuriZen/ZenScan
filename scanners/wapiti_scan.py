from wapitiCore.main.wapiti import Wapiti

def run_wapiti_scan(target):
    wapiti = Wapiti(target)
    wapiti.attack()
