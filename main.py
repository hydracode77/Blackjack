from random import choice
import pygame
from sys import exit

# pygame start
pygame.init()
screen = pygame.display.set_mode((1200, 701))
clock = pygame.time.Clock()

bg_music = pygame.mixer.Sound("graphics/musik.mp3")
bg_music.set_volume(0.03)
bg_music.play()

mute = False
able_to_reset = False  # man darf nur dann resetten, wenn die runde fertig ist
gewinn_calculated = False  # damit nur einmal Gewinn verdoppelt/oder den Einsatz zurückgegeben wird
mouse_pressed = False  # für chips, damit man bei 1x klicken, auch nur 1 Chips setzt
start_index = 0   # 1x Enter drücken -> next (am start eines spiels)
table_overlay = pygame.image.load("graphics/Table/table.jpg").convert()
table_zwei_cards = pygame.image.load("graphics//Table/table_2cards.jpg").convert()
player_end_num = 0
round_finished = False


class Cards:
    class Shippe:  # fail ich weiß, hätte pik nehmen sollen
        ass = pygame.image.load("graphics/Shippe/Ass.png").convert()
        zwei = pygame.image.load("graphics/Shippe/2.png").convert()
        drei = pygame.image.load("graphics/Shippe/3.png").convert()
        vier = pygame.image.load("graphics/Shippe/4.png").convert()
        funf = pygame.image.load("graphics/Shippe/5.png").convert()
        sechs = pygame.image.load("graphics/Shippe/6.png").convert()
        sieben = pygame.image.load("graphics/Shippe/7.png").convert()
        acht = pygame.image.load("graphics/Shippe/8.png").convert()
        neun = pygame.image.load("graphics/Shippe/9.png").convert()
        zehn = pygame.image.load("graphics/Shippe/10.png").convert()
        queen = pygame.image.load("graphics/Shippe/queen.png").convert()
        king = pygame.image.load("graphics/Shippe/king.png").convert()
        bube = pygame.image.load("graphics/Shippe/bube.png").convert()

    class Kreuz:
        ass = pygame.image.load("graphics/Kreuz/Ass.png").convert()
        zwei = pygame.image.load("graphics/Kreuz/2.png").convert()
        drei = pygame.image.load("graphics/Kreuz/3.png").convert()
        vier = pygame.image.load("graphics/Kreuz/4.png").convert()
        funf = pygame.image.load("graphics/Kreuz/5.png").convert()
        sechs = pygame.image.load("graphics/Kreuz/6.png").convert()
        sieben = pygame.image.load("graphics/Kreuz/7.png").convert()
        acht = pygame.image.load("graphics/Kreuz/8.png").convert()
        neun = pygame.image.load("graphics/Kreuz/9.png").convert()
        zehn = pygame.image.load("graphics/Kreuz/10.png").convert()
        queen = pygame.image.load("graphics/Kreuz/queen.png").convert()
        king = pygame.image.load("graphics/Kreuz/king.png").convert()
        bube = pygame.image.load("graphics/Kreuz/bube.png").convert()

    class Herz:
        ass = pygame.image.load("graphics/Herz/Ass.png").convert()
        zwei = pygame.image.load("graphics/Herz/2.png").convert()
        drei = pygame.image.load("graphics/Herz/3.png").convert()
        vier = pygame.image.load("graphics/Herz/4.png").convert()
        funf = pygame.image.load("graphics/Herz/5.png").convert()
        sechs = pygame.image.load("graphics/Herz/6.png").convert()
        sieben = pygame.image.load("graphics/Herz/7.png").convert()
        acht = pygame.image.load("graphics/Herz/8.png").convert()
        neun = pygame.image.load("graphics/Herz/9.png").convert()
        zehn = pygame.image.load("graphics/Herz/10.png").convert()
        queen = pygame.image.load("graphics/Herz/queen.png").convert()
        king = pygame.image.load("graphics/Herz/king.png").convert()
        bube = pygame.image.load("graphics/Herz/bube.png").convert()

    class Karo:
        ass = pygame.image.load("graphics/Karo/Ass.png").convert()
        zwei = pygame.image.load("graphics/Karo/2.png").convert()
        drei = pygame.image.load("graphics/Karo/3.png").convert()
        vier = pygame.image.load("graphics/Karo/4.png").convert()
        funf = pygame.image.load("graphics/Karo/5.png").convert()
        sechs = pygame.image.load("graphics/Karo/6.png").convert()
        sieben = pygame.image.load("graphics/Karo/7.png").convert()
        acht = pygame.image.load("graphics/Karo/8.png").convert()
        neun = pygame.image.load("graphics/Karo/9.png").convert()
        zehn = pygame.image.load("graphics/Karo/10.png").convert()
        queen = pygame.image.load("graphics/Karo/queen.png").convert()
        king = pygame.image.load("graphics/Karo/king.png").convert()
        bube = pygame.image.load("graphics/Karo/bube.png").convert()

    full_list = [Shippe.ass, Shippe.zwei, Shippe.drei, Shippe.vier, Shippe.funf, Shippe.sechs, Shippe.sieben,
                 Shippe.acht, Shippe.neun, Shippe.zehn, Shippe.queen, Shippe.king, Shippe.bube,
                 Kreuz.ass, Kreuz.zwei, Kreuz.drei, Kreuz.vier, Kreuz.funf, Kreuz.sechs, Kreuz.sieben, Kreuz.acht,
                 Kreuz.neun, Kreuz.zehn, Kreuz.queen, Kreuz.king, Kreuz.bube,
                 Herz.ass, Herz.zwei, Herz.drei, Herz.vier, Herz.funf, Herz.sechs, Herz.sieben, Herz.acht, Herz.neun,
                 Herz.zehn, Herz.queen, Herz.king, Herz.bube,
                 Karo.ass, Karo.zwei, Karo.drei, Karo.vier, Karo.funf, Karo.sechs, Karo.sieben, Karo.acht, Karo.neun,
                 Karo.zehn, Karo.queen, Karo.king, Karo.bube]

    ass_list = [Shippe.ass, Kreuz.ass, Herz.ass, Karo.ass]
    zwei_list = [Shippe.zwei, Kreuz.zwei, Herz.zwei, Karo.zwei]
    drei_list = [Shippe.drei, Kreuz.drei, Herz.drei, Karo.drei]
    vier_list = [Shippe.vier, Kreuz.vier, Herz.vier, Karo.vier]
    funf_list = [Shippe.funf, Kreuz.funf, Herz.funf, Karo.funf]
    sechs_list = [Shippe.sechs, Kreuz.sechs, Herz.sechs, Karo.sechs]
    sieben_list = [Shippe.sieben, Kreuz.sieben, Herz.sieben, Karo.sieben]
    acht_list = [Shippe.acht, Kreuz.acht, Herz.acht, Karo.acht]
    neun_list = [Shippe.neun, Kreuz.neun, Herz.neun, Karo.neun]
    zehn_list = [Shippe.zehn, Kreuz.zehn, Herz.zehn, Karo.zehn, Shippe.king, Kreuz.king, Herz.king, Karo.king, Shippe.queen, Kreuz.queen, Herz.queen, Karo.queen, Shippe.bube, Kreuz.bube, Herz.bube, Karo.bube]

    card1 = choice(full_list)
    card2 = choice(full_list)
    card3 = None
    card4 = None
    card5 = None

    current_deck = [card1, card2]  # standartmäßig 2, können später erweitert werden
    get = True   # auslosen der karten
    ass_innit = 0   # wie viele asse hat das current_deck


class Enemy:
    # besondere Liste für Enemy damit er mind 14 aus 2 Karten hat
    card_list = [Cards.Shippe.ass, Cards.Kreuz.ass, Cards.Herz.ass, Cards.Karo.ass, Cards.Shippe.acht, Cards.Kreuz.acht, Cards.Herz.acht, Cards.Karo.acht, Cards.Shippe.neun, Cards.Kreuz.neun, Cards.Herz.neun, Cards.Karo.neun, Cards.Shippe.zehn, Cards.Kreuz.zehn, Cards.Herz.zehn, Cards.Karo.zehn, Cards.Shippe.sieben, Cards.Kreuz.sieben, Cards.Herz.sieben, Cards.Karo.sieben, Cards.Shippe.king, Cards.Kreuz.king, Cards.Herz.king, Cards.Karo.king]
    card1 = choice(card_list)
    card2 = choice(card_list)
    while card1 in Cards.ass_list and card2 in Cards.ass_list:  # damit enemy nicht 2 asse haben kann
        card2 = choice(card_list)
    picked_cards = [card1, card2]
    end_num = 0  # finale Punkte
    for card in picked_cards:  # Berechnung der Punkte
        if card in Cards.ass_list:
            end_num += 11
        elif card in Cards.sieben_list:
            end_num += 7
        elif card in Cards.acht_list:
            end_num += 8
        elif card in Cards.neun_list:
            end_num += 9
        elif card in Cards.zehn_list:
            end_num += 10


class Chips:
    zehn = pygame.image.load("graphics/chips/10.png").convert_alpha()
    zehn_rect = zehn.get_rect(topleft=(394, 322))
    zwanzig = pygame.image.load("graphics/chips/20.png").convert_alpha()
    zwanzig_rect = zehn.get_rect(topleft=(484, 322))
    funfzig = pygame.image.load("graphics/chips/50.png").convert_alpha()
    funfzig_rect = zehn.get_rect(topleft=(575, 322))
    hundert = pygame.image.load("graphics/chips/100.png").convert_alpha()
    hundert_rect = zehn.get_rect(topleft=(666, 322))
    funfhundert = pygame.image.load("graphics/chips/500.png").convert_alpha()
    funfhundert_rect = zehn.get_rect(topleft=(757, 322))
    money = 1000
    current_einsatz = 0
    list = []  # Liste an gesetzten Chips
    einsatz_place_x = 575  # Platz an dem gesetzte Chips beim setzen gezeigt werden
    rect_list = [zehn_rect, zwanzig_rect, funfzig_rect, hundert_rect, funfhundert_rect]


class Text:
    normal_font = pygame.font.Font("graphics/BAUHS93.TTF", 85)
    money_font = pygame.font.Font("graphics/BAUHS93.TTF", 60)
    money_text = money_font.render(f"{Chips.money}", True, (255, 215, 0))
    win_text = normal_font.render("YOU WIN!", True, (0, 0, 0))
    lose_text = normal_font.render("YOU LOSE!", True, (0, 0, 0))
    draw_text = normal_font.render("DRAW!", True, (0, 0, 0))
    plus_0 = money_font.render("+0", True, (0, 0, 0))
    plus_win = money_font.render(f"+{Chips.current_einsatz * 2}", True, (255, 215, 0))
    plus_rect = plus_win.get_rect(midbottom=(570, 119))
    keybind_text = pygame.image.load("graphics/keybind_button.png").convert_alpha()
    keybind_text = pygame.transform.rotozoom(keybind_text, 0, 0.5)
    keybind_rect = keybind_text.get_rect(topleft=(20, 20))
    keybind_full_text = pygame.image.load("graphics/keybinds_full_text.png").convert()
    keybind_full_text = pygame.transform.rotozoom(keybind_full_text, 0, 0.35)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Runde beendet. Bitte besuchen Sie uns bald wieder!")
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if not mute:
                    bg_music.set_volume(0)  # Musik muten
                    mute = True
                else:
                    bg_music.set_volume(0.03)  # Musik unmuten
                    mute = False

            if event.key == pygame.K_SPACE:
                start_index += 1
                if start_index == 2:
                    Chips.money -= Chips.current_einsatz

            if event.key == pygame.K_KP_PLUS and not round_finished and start_index > 1: # nur Karte ziehen wenn Runde nd zu ende, aber Chips schon gelegt
                # neue Karte ziehen (Hit)
                if Cards.card3 is None:
                    Cards.card3 = choice(Cards.full_list)
                elif Cards.card4 is None:
                    Cards.card4 = choice(Cards.full_list)
                elif Cards.card5 is None:
                    Cards.card5 = choice(Cards.full_list)

            if event.key == pygame.K_RETURN and start_index > 1: # the same
                round_finished = True
                # Runde beenden (Stand)
                able_to_reset = True
                for card in Cards.current_deck:
                    if card in Cards.ass_list:
                        player_end_num += 11
                        Cards.ass_innit += 1
                    elif card in Cards.zwei_list:
                        player_end_num += 2
                    elif card in Cards.drei_list:
                        player_end_num += 3
                    elif card in Cards.vier_list:
                        player_end_num += 4
                    elif card in Cards.funf_list:
                        player_end_num += 5
                    elif card in Cards.sechs_list:
                        player_end_num += 6
                    elif card in Cards.sieben_list:
                        player_end_num += 7
                    elif card in Cards.acht_list:
                        player_end_num += 8
                    elif card in Cards.neun_list:
                        player_end_num += 9
                    elif card in Cards.zehn_list:
                        player_end_num += 10
                if player_end_num > 21 and Cards.ass_innit > 0:
                    for i in range(0, Cards.ass_innit):
                        if player_end_num > 21:
                            player_end_num -= 10
                    Cards.ass_innit = 0

            if event.key == pygame.K_KP_ENTER and able_to_reset:
                # neues Game
                round_finished = False
                Cards.get = True
                start_index = 0
                Cards.card3 = None
                Cards.card4 = None
                Cards.card5 = None
                Cards.current_deck = [Cards.card1, Cards.card2]
                player_end_num = 0
                able_to_reset = False
                Enemy.card1 = choice(Enemy.card_list)
                Enemy.card2 = choice(Enemy.card_list)
                while Enemy.card1 in Cards.ass_list and Enemy.card2 in Cards.ass_list:  # damit enemy nicht 2 asse haben kann
                    Enemy.card2 = choice(Enemy.card_list)
                Cards.card1 = choice(Cards.full_list)
                Cards.card2 = choice(Cards.full_list)
                Enemy.picked_cards = [Enemy.card1, Enemy.card2]
                Enemy.end_num = 0
                for card in Enemy.picked_cards:
                    if card in Cards.ass_list:
                        Enemy.end_num += 11
                    elif card in Cards.sieben_list:
                        Enemy.end_num += 7
                    elif card in Cards.acht_list:
                        Enemy.end_num += 8
                    elif card in Cards.neun_list:
                        Enemy.end_num += 9
                    elif card in Cards.zehn_list:
                        Enemy.end_num += 10
                Chips.current_einsatz = 0
                Chips.list = []
                gewinn_calculated = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_state = pygame.mouse.get_pressed()

    # leertaste drücken um zu skippen (start jeder Runde)
    if start_index == 0:
        screen.blit(table_overlay, (0, 0))  # leerer Spieltisch
    if start_index == 1:
        screen.blit(table_overlay, (0, 0))  # Spieltisch mit Chips zum setzten
        screen.blit(Chips.zehn, Chips.zehn_rect)
        screen.blit(Chips.zwanzig, Chips.zwanzig_rect)
        screen.blit(Chips.funfzig, Chips.funfzig_rect)
        screen.blit(Chips.hundert, Chips.hundert_rect)
        screen.blit(Chips.funfhundert, Chips.funfhundert_rect)

        # Chips anklicken zum Setzen
        for rect in Chips.rect_list:
            if mouse_state[0] and not mouse_pressed:  # damit man bei 1x klicken 1 Chip setzt gibt es mouse_pressed
                if rect.collidepoint(mouse_pos):
                    mouse_pressed = True
                    if rect == Chips.rect_list[0]:  # falls es sich um den 10er Chip handelt
                        Chips.current_einsatz += 10  # Einsatz um 10 erhöhen
                        if Chips.current_einsatz > Chips.money:  # falls mehr wettet, als geld hat, wird abgezogen
                            Chips.current_einsatz -= 10
                        else:
                            Chips.list.append(Chips.zehn)  # Chip list erweitern um 10

                    if rect == Chips.rect_list[1]:
                        Chips.current_einsatz += 20
                        if Chips.current_einsatz > Chips.money:
                            Chips.current_einsatz -= 20
                        else:
                            Chips.list.append(Chips.zwanzig)

                    if rect == Chips.rect_list[2]:
                        Chips.current_einsatz += 50
                        if Chips.current_einsatz > Chips.money:
                            Chips.current_einsatz -= 50
                        else:
                            Chips.list.append(Chips.funfzig)

                    if rect == Chips.rect_list[3]:
                        Chips.current_einsatz += 100
                        if Chips.current_einsatz > Chips.money:
                            Chips.current_einsatz -= 100
                        else:
                            Chips.list.append(Chips.hundert)

                    if rect == Chips.rect_list[4]:
                        Chips.current_einsatz += 500
                        if Chips.current_einsatz > Chips.money:
                            Chips.current_einsatz -= 500
                        else:
                            Chips.list.append(Chips.funfhundert)

            elif not mouse_state[0] and mouse_pressed:  # nochmal überprüfen, ob maus geklickt, wenn nicht, dann False
                mouse_pressed = False

        # alle gesetzten Chips so blitten, als lägen sie übereinander
        for chip in Chips.list:
            screen.blit(chip, (Chips.einsatz_place_x, 206))
            Chips.einsatz_place_x += 7
        Chips.einsatz_place_x = 575

    if start_index == 2:  # Player cards umgedreht, eine Enemy Card wird gezeigt
        screen.blit(table_zwei_cards, (0, 0))
        screen.blit(Enemy.card1, (506, 157))
    if start_index == 3:  # eine Player Card aufdecken
        screen.blit(table_zwei_cards, (0, 0))
        screen.blit(Enemy.card1, (506, 157))
        screen.blit(Cards.card1, (506, 441))
    if start_index >= 4:  # zweite Player Card aufdecken
        screen.blit(table_zwei_cards, (0, 0))
        screen.blit(Enemy.card1, (506, 157))
        screen.blit(Cards.card1, (506, 441))
        screen.blit(Cards.card2, (620, 441))

    # standart blitten
    # alles hier wird immer angezeigt
    Text.plus_win = Text.money_font.render(f"+{Chips.current_einsatz * 2}", True, (255, 215, 0))  # neue Berechnung
    Text.money_text = Text.money_font.render(f"{Chips.money}", True, (255, 215, 0))
    screen.blit(Text.money_text, (1020, 20))
    screen.blit(Text.keybind_text, Text.keybind_rect)
    if Text.keybind_rect.collidepoint(mouse_pos):
        screen.blit(Text.keybind_full_text, (20, 20))

    # weitere Karten blitten
    if Cards.card3 is not None:  # falls card3 ein wert hat, also aufgedeckt wurde, gehört sie zum deck
        Cards.current_deck = [Cards.card1, Cards.card2, Cards.card3]
        screen.blit(Cards.card3, (392, 441))
    if Cards.card4 is not None:  # danach wird gecheckt ob card4 ein wert hat. Ist es so, wird deck korrigiert
        Cards.current_deck = [Cards.card1, Cards.card2, Cards.card3, Cards.card4]
        screen.blit(Cards.card4, (734, 441))
    if Cards.card5 is not None:
        Cards.current_deck = [Cards.card1, Cards.card2, Cards.card3, Cards.card4, Cards.card5]
        screen.blit(Cards.card5, (567, 331))
    if Cards.card3 is None and Cards.card4 is None and Cards.card5 is None:  # wenn alle anderen karten keinen Wert haben, besteht das deck nur aus 2 karten
        Cards.current_deck = [Cards.card1, Cards.card2]

    # Auswertung: Wer hat gewonnen?
    if player_end_num > 0:  # wenn Player_end_num berechnet wurde
        screen.blit(Enemy.card2, (620, 157))  # zweite Karte von Enemy zeigen

        if player_end_num > 21 or player_end_num < Enemy.end_num:  # ist man über 21 oder kleiner als der Enemy
            screen.blit(Text.lose_text, (400, 300))  # Verloren!

        elif player_end_num == Enemy.end_num:  # ist end_num gleich groß wie beim enemy:
            screen.blit(Text.draw_text, (460, 300))  # unentschieden
            screen.blit(Text.plus_0, Text.plus_rect)
            if not gewinn_calculated:  # schutz damit es nicht mehrmals ausgezahlt wird
                Chips.money += Chips.current_einsatz  # Einsatz wieder zurückgeben
                gewinn_calculated = True

        elif player_end_num > Enemy.end_num:  # mehr als Enemy:
            screen.blit(Text.win_text, (410, 300))  # Gewonnen!
            screen.blit(Text.plus_win, Text.plus_rect)  # wie viel man gewonnen hat, wird gezeigt
            if not gewinn_calculated:  # schutz damit es nicht mehrmals ausgezahlt wird
                Chips.money += Chips.current_einsatz * 2  # Einsatz verdoppeln
                gewinn_calculated = True

    pygame.display.update()
    try:
        clock.tick(60)
    except KeyboardInterrupt:
        print("Runde beendet. Bitte besuchen Sie uns bald wieder!")
        pygame.quit()
        exit()

