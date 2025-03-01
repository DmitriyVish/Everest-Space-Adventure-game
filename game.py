import pygame 
import random

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 686)) # Экран
pygame.display.set_caption('Game') # Название приложения
icon = pygame.image.load('images/icon.png') # подгрузка иконки
pygame.display.set_icon(icon) # установка иконки

"""Изображения"""
back = pygame.image.load('images/background.jpg').convert() # подгрузка фона
win_img = pygame.transform.scale(pygame.image.load('images/space_ship.jpg').convert(), (1920, 686))
lose_img = pygame.transform.scale(pygame.image.load('images/ghost.jpg').convert(), (1920, 686))
player_right = pygame.image.load('images/everest_11zon_inv.png').convert_alpha() # подгрузка игрока направление вправо
player_left = pygame.image.load('images/everest_11zon.png').convert_alpha() # подгрузка игрока направление влево
monster = pygame.image.load('images/monster.png').convert_alpha() # подгружаем монстра
puppy = pygame.transform.scale(pygame.image.load('images/puppy.png').convert_alpha(), (80, 80)) # подгружаем щеночка
bullet = pygame.image.load('images/bullet.png').convert_alpha() # подгружаем картинку снаряда 

"""Музыка"""
bg_sound = pygame.mixer.Sound('sounds/Loyalty_Freak_Music.mp3') # подгрузка звука
bg_sound.play() # проигрывание звука

"""Переменные и списки"""
bg_x = 0 # х коородината фона
# движение вправо - влево
player_speed = 5 #  скорость передвижения игрока
player_x = 200 # х координата игрока

# прыжок
player_y = 500 # y координата игрока
is_jump = False # флаг прыжка
jump_count = 12 # при прыжке поднимем и опускаем игрока на n позиций (высота прыжка)

monster_x = 1925 # х координата монстра (появляется за пределами экрана)
monster_y = 480
monster_list = [] # список для монстров

# Стрельба по монстрам
bullets_left = 10 # Ограничение количества снарядов
bullets = [] # выпущенные патроны
bullets_count = 9

# Щеночки
puppy_list = []
puppy_x = 1920
puppy_count = 0

"""Флаги"""
win = True
gameplay = True
running = True

"""Таймеры"""

# Таймер для появления монстров
monster_timer = pygame.USEREVENT + 1
pygame.time.set_timer(monster_timer, 2500) # появление монстра через 2.5 сек
puppy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(puppy_timer, 5000)

"""Тексты"""
label = pygame.font.Font('fonts/AtkinsonHyperlegibleMono-Regular.ttf', 70)

lose_label = label.render("YOU LOSE!!!", True, ('red'))
won_label = label.render("WELL DONE!!! ALL PUPPIES SAVED", True, ('green'))

restart_label = label.render("PLAY AGAIN?", True, ('blue'))
restart_label_rect = restart_label.get_rect(topleft=(780, 400))

label_text = pygame.font.Font('fonts/AtkinsonHyperlegibleMono-Regular.ttf', 40)

bullets_label = label_text.render("BULLETS", True, ('red'))
bullets_label_rect = bullets_label.get_rect(topleft=(10, 30))  
bullets_label_count = label_text.render("10", True, ('red'))
bullets_label_count_rect = bullets_label_count.get_rect(topleft=(10, 70))

puppy_label = label_text.render("PUPPIES", True, ('green'))
puppy_label_rect = bullets_label.get_rect(topleft=(200, 30))  
puppy_label_count = label_text.render("10", True, ('green'))
puppy_label_count_rect = bullets_label_count.get_rect(topleft=(200, 70))


"""Игровой цикл"""
while running:    
    # Отрисовка фона
    screen.blit(back, (bg_x, 0)) # отображаем 1 фон
    screen.blit(back, (bg_x + 1920, 0)) # отображаем 2 фон   
    # Движение фона
    bg_x -= 2 # изменяем начальную координату х фона
    if bg_x == -1920: # если фон сместился до границы х
        bg_x = 0 # сбрасываем координату фона
        
    # Условие проигрыша
    if gameplay: 
        # отрисовываем тексты снарядов
        screen.blit(bullets_label, bullets_label_rect)       
        screen.blit(bullets_label_count, bullets_label_count_rect)   
        # отрисовываем тексты щеночков
        screen.blit(puppy_label, puppy_label_rect)
        screen.blit(puppy_label_count, puppy_label_count_rect)     
        
        # Соприкосновение изображений
        # Отрисовка квадрата для каждого изображения
        player_rect = player_right.get_rect(topleft=(player_x, player_y))
        # monster_rect = player_right.get_rect(topleft=(monster_x, monster_y))
            
        # Проверяем наличие монстров в списке
        if monster_list:
            for i, elem in enumerate(monster_list):
                screen.blit(monster, elem) # отрисовываем монстра в координатах появления его квадрата
                elem.x -= 10 # перемещаем монстра                  
                
                if elem.x < 0: # если монстр за дисплеем
                    monster_list.pop(i)
            
            # Отслеживание соприкосновений
            if player_rect.colliderect(elem):
                win = False
                # print('YOU LOSE!!!')
                gameplay = False
                
        # Проверяем наличие щенков в списке
        if puppy_list:
            for i, puppy_elem in enumerate(puppy_list):
                screen.blit(puppy, puppy_elem) # отрисовываем щеночка в координатах появления его квадрата
                puppy_elem.x -= 5 # перемещаем щеночка
                if puppy_elem.x < 0: # если щеночек на границе экрана, удаляем из списка
                    puppy_list.pop(i)
                    # Отслеживаем соприкосновение игрока и щеночка
                if player_rect.colliderect(puppy_elem): 
                    if puppy_count < 10:
                        puppy_list.pop(i) # удаляем щеночка из списка
                        puppy_count += 1 # Увеличиваем количество щеночков на 1                    
                    if puppy_count == 10: # Если собрано 10 щеночков, игра окончена
                        win = True
                        # print('YOU WON!!!')
                        gameplay = False                 
                        break
        
        keys = pygame.key.get_pressed() # получаем нажатые кнопки
        
        # Отображение и поворот игрока    
        if keys[pygame.K_LEFT]: # усли клавиша влево
            screen.blit(player_left, (player_x, player_y)) # отображаем игрока влево
        else:
            screen.blit(player_right, (player_x, player_y)) # отображаем игрока вправо
        
        screen.blit(monster, (monster_x, monster_y)) # отображение монстра
        #monster_x -= 10 # передвижение монстра
        
        # Движение
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed # двигаем игрока влево
        elif keys[pygame.K_RIGHT] and player_x < 1100:
            player_x += player_speed # двигаем игрока вправо
        # Прыжок
        if not is_jump: # проверка на прыжок 
            if keys[pygame.K_UP]: # если нажата кнопка вверх
                is_jump = True # меняем флаг на True
        else: # если игрок уже прыгает 
            if jump_count >= -12: # если прыжок не закончился
                if jump_count > 0: # если > 0
                    player_y -= (jump_count ** 2) / 2 # поднимаем игрока (** 2 мощнее прыжок) (/ 2 плавнее подъем)
                else:
                    player_y += (jump_count ** 2) / 2 # опускаем игрока (** 2 мощнее прыжок) (/ 2 плавнее спад)
                jump_count -= 1 # меняем высоту прыжка
            else: # если вышли за диапазон
                is_jump = False # меняем флаг на False
                jump_count = 12 # сбрасываем высоту прыжка    
        # отслеживание выстрела 
        # if keys[pygame.K_SPACE]: # если нажат пробел
            # передаем квадрат вокруг снаряда
            # bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10))) # картинка появляется в координатах игрока
        if bullets: # проверяем есть ли снаряды в списке
            for i, elem in enumerate(bullets): # перебираем список
                screen.blit(bullet, (elem.x, elem.y)) # отрисовываем снаряды в координатах их появления
                elem.x += 16 # перемещаем снаряд 
                
                if elem.x > 1921: # если снаряд достиг границы экрана
                   bullets.pop(i) # удаляем снаряд из списка
                   
                # Соприкосновение с монстрами
                if monster_list: # проверяем есть ли монстры в игре
                    for index, monster_el in enumerate(monster_list):
                        if elem.colliderect(monster_el): # если снаряд пересекается с монстром
                            # удаляем монстра и снаряд
                            monster_list.pop(index)                          
                            bullets.pop(i) # удаляем снаряд
                            bullets_count -= 1
                            break # выходим из внутреннего цикла
    #  Игра окончена
    else:
        # Экран выигрыша
        if win:
            screen.blit(win_img, (0, 0)) 
            screen.blit(won_label, (400, 300))
            screen.blit(restart_label, restart_label_rect)
        # Экран проигрыша
        else: 
            screen.blit(lose_img, (0, 0)) 
            screen.blit(lose_label, (780, 300))
            screen.blit(restart_label, restart_label_rect)
        
        # Рестарт игры
        mouse = pygame.mouse.get_pos() # координаты мышки
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]: # если курсор находится внутри кнопки
            gameplay = True # запускаем игру
            player_x = 200 # переносим игрока в первоначальное положение
            monster_list.clear() # очищаем список с монстрами
            bullets.clear() # очищаем список со снарядами
            # bullets_left = 10 # обновляем количество снарядов
            bullets_count = 10 # обновляем количество снарядов
            puppy_list.clear() # очищаем список щеночков
            puppy_count = 0 # обнуляем количество щеночков
    
    pygame.display.update() # Обновление экрана
    
    for event in pygame.event.get():
        # Отслеживание таймера монстров
        if event.type == monster_timer:
            monster_list.append(monster.get_rect(topleft=(monster_x, random.choice(range(200, 480))))) # добавляем монстра в список
        # Отслеживание выстрела
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_count > 0: # если находимся в игре и была нажата и отпущена клавиша
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10))) # картинка появляется в координатах игрока 
            # bullets_count -= 1 # убираем по 1 снаряду 
            if bullets_count > -1:
                bullets_label_count = label_text.render(str(bullets_count), True, 'red')                
        if event.type == puppy_timer:
            puppy_list.append(puppy.get_rect(topleft=(puppy_x, random.choice(range(150, 400)))))
            if puppy_count <= 10:
                puppy_label_count = label_text.render(str(puppy_count), True, 'green')             
               
        if event.type == pygame.QUIT: # Остановка игры
            running = False
            pygame.quit()
    clock.tick(50)