def main_menu():        
    screen.fill(BLACK)
    title_text = font.render("SUPERFIGHTERS",True , WHITE)
    screen.blit(title_text, (resolution[0] // 2 - title_text.get_width() // 2, resolution[1] // 2 - title_text.get_height() // 2))
    button.draw(screen)
