import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack - Multiplayer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)
background_image = pygame.image.load("./background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH,HEIGHT))

def create_deck():
    global deck
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♣', '♦', '♥']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    score = 0
    num_aces = 0
    for card in hand:
        rank = card[0]
        if rank.isdigit():
            score += int(rank)
        elif rank in ['J', 'Q', 'K']:
            score += 10
        else:  # Ace
            num_aces += 1
            score += 11
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_card(card, x, y):
    card_image = pygame.image.load(f"cards/{card[1]}{card[0]}.png")
    card_image = pygame.transform.scale(card_image, (100, 150))
    screen.blit(card_image, (x, y))

def end_game_screen(player1_score, player2_score, dealer_score):
    screen.fill(BLACK)
    draw_text("Game Over", font, WHITE, 300, 150)
    draw_text("Player 1 Score: " + str(player1_score), font, WHITE, 300, 200)
    draw_text("Player 2 Score: " + str(player2_score), font, WHITE, 300, 250)
    draw_text("Dealer's Score: " + str(dealer_score), font, WHITE, 300, 300)
    winner_text = ""
    if player1_score == 21:
        winner_text = "Player 1 has Blackjack! Player 1 wins!"
    elif player2_score == 21:
        winner_text = "Player 2 has Blackjack! Player 2 wins!"
    elif player1_score > 21 and player2_score > 21:
        winner_text = "Both players bust. Dealer wins!"
    elif player1_score > 21:
        winner_text = "Player 1 busts. Player 2 wins!"
    elif player2_score > 21:
        winner_text = "Player 2 busts. Player 1 wins!"
    elif dealer_score > 21:
        winner_text = "Dealer busts. Both players win!"
    elif player1_score > player2_score:
        winner_text = "Player 1 wins!"
    elif player2_score > player1_score:
        winner_text = "Player 2 wins!"
    else:
        winner_text = "It's a tie!"

    draw_text(winner_text, font, WHITE, 300, 350)

    pygame.draw.rect(screen, GREEN, (200, 400, 150, 50))
    draw_text("Restart", font, WHITE, 230, 412)
    pygame.draw.rect(screen, RED, (450, 400, 150, 50))
    draw_text("Quit", font, WHITE, 497, 412)
    pygame.display.flip()

def restart_game():
    return create_deck(), [deck.pop(), deck.pop()], [deck.pop(), deck.pop()], [deck.pop(), deck.pop()], True

def blackjack():
    deck, player1_hand, player2_hand, dealer_hand, running = restart_game()

    card_back = pygame.image.load("cards/back.png")
    card_back = pygame.transform.scale(card_back, (100, 150))

    current_player = 1
    while True:
        screen.blit(background_image, (0, 0))
        
        if current_player == 1:
            draw_text("Player 1 Hand:", font, WHITE, 50, 50)
            player_hand = player1_hand
        else:
            draw_text("Player 2 Hand:", font, WHITE, 50, 50)
            player_hand = player2_hand

        x, y = 50, 100
        for card in player_hand:
            draw_card(card, x, y)
            x += 120

        draw_text("Dealer's Hand:", font, WHITE, 50, 300)
        draw_card(dealer_hand[0], 50, 350)
        if running and current_player == 1 or current_player == 2 :
            screen.blit(card_back, (170, 350))

        player1_score = calculate_score(player1_hand)
        player2_score = calculate_score(player2_hand)
        dealer_score = calculate_score(dealer_hand)
        if current_player == 1:
            draw_text("Player 1 Score: " + str(player1_score), font, WHITE, 50, 550)
        else:
            draw_text("Player 2 Score: " + str(player2_score), font, WHITE, 50, 550)

        if player1_score == 21 or player2_score == 21:
            running = False
            end_game_screen(player1_score, player2_score, dealer_score)
            break

        if (player1_score > 21 and current_player == 1) or (player2_score > 21 and current_player == 2) or not running:
            while dealer_score < 17:
                dealer_hand.append(deck.pop())
                dealer_score = calculate_score(dealer_hand)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and current_player == 1:
                if event.key == pygame.K_h and running:
                    player1_hand.append(deck.pop())
                elif event.key == pygame.K_s and running:
                    current_player = 2
            elif event.type == pygame.KEYDOWN and current_player == 2:
                if event.key == pygame.K_h and running:
                    player2_hand.append(deck.pop())
                elif event.key == pygame.K_s and running:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not running:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 200 <= mouse_x <= 350 and 400 <= mouse_y <= 450:
                    player1_score,player2_score,dealer_score=0,0,0
                    current_player = 1
                    blackjack()
                elif 450 <= mouse_x <= 600 and 400 <= mouse_y <= 450:
                    pygame.quit()
                    sys.exit()

        if not running:
            end_game_screen(player1_score, player2_score, dealer_score)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if (200 <= mouse_x <= 350 and 400 <= mouse_y <= 450):
                            player1_score,player2_score,dealer_score=0,0,0
                            current_player = 1
                            blackjack()
                            break
                        elif (450 <= mouse_x <= 600 and 400 <= mouse_y <= 450):
                            pygame.quit()
                            sys.exit()
                    elif (event.type == pygame.QUIT):
                        pygame.quit()
                        sys.exit()
                        
blackjack()
