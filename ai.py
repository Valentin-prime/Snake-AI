from snake import Snake, spawn_apple
import pygame
import random
import pickle

# Constants
WINDOW_SIZE = (400, 400)
PIXEL_SIZE = 20
ACTIONS = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
Q_TABLE_FILE = "50k_82_31.pkl"

def get_state(snake: Snake, apple):
    head_x, head_y = snake.head
    apple_x, apple_y = apple
    
    return (
        head_x < apple_x,  # Apple is to the right
        head_x > apple_x,  # Apple is to the left
        head_y < apple_y,  # Apple is below
        head_y > apple_y,  # Apple is above
        snake.direction == 'left',
        snake.direction == 'right',
        snake.direction == 'up',
        snake.direction == 'down',
        (head_x - PIXEL_SIZE, head_y) in snake.get_body_pos() or head_x - PIXEL_SIZE < 0,  # Wall or body left
        (head_x + PIXEL_SIZE, head_y) in snake.get_body_pos() or head_x + PIXEL_SIZE >= WINDOW_SIZE[0],  # Wall or body right
        (head_x, head_y - PIXEL_SIZE) in snake.get_body_pos() or head_y - PIXEL_SIZE < 0,  # Wall or body up
        (head_x, head_y + PIXEL_SIZE) in snake.get_body_pos() or head_y + PIXEL_SIZE >= WINDOW_SIZE[1]   # Wall or body down
    )

class SnakeAI:
    def __init__(self, epsilon):
        self.q_table = self.load_q_table()
        self.epsilon = epsilon
        self.learning_rate = 0.1
        self.discount_factor = 0.9

    def load_q_table(self):
        try:
            with open(Q_TABLE_FILE, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_q_table(self):
        with open(Q_TABLE_FILE, "wb") as f:
            pickle.dump(self.q_table, f)

    def choose_action(self, state, current_direction):
        valid_actions = [a for a in ACTIONS if ACTIONS[a] != current_direction]  # Exclude opposite direction
        
        if random.uniform(0, 1) < self.epsilon or state not in self.q_table:
            return random.choice(valid_actions)
        
        q_values = {a: self.q_table[state].get(a, 0) for a in valid_actions}
        return max(q_values, key=q_values.get)

    def update_q_value(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in ACTIONS}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in ACTIONS}
        
        old_q = self.q_table[state][action]
        max_future_q = max(self.q_table[next_state].values())
        new_q = old_q + self.learning_rate * (reward + self.discount_factor * max_future_q - old_q)
        self.q_table[state][action] = new_q

def run_game(visible=True, episodes=1):
    pygame.init()
    pygame.event.pump()
    screen = pygame.display.set_mode(WINDOW_SIZE) if visible else None
    clock = pygame.time.Clock()
    ai = SnakeAI(int(not visible))
    best_score = 0
    total_score = 0
    
    for episode in range(episodes):
        snake = Snake(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2, PIXEL_SIZE)
        apple = spawn_apple(WINDOW_SIZE, PIXEL_SIZE, snake)
        game_over = False
        score = 0

        if not episode % 1000:
            ai.epsilon *= 0.1
        
        while not game_over:
            state = get_state(snake, apple)
            action = ai.choose_action(state, snake.direction)
            snake.direction = action
            snake.move()
            
            reward = -1
            if snake.head == apple:
                apple = spawn_apple(WINDOW_SIZE, PIXEL_SIZE, snake)
                snake.size += 1
                reward = snake.size - 2
                score += 1
            elif snake.head in snake.get_body_pos()[1:] or \
                 not (0 <= snake.head[0] < WINDOW_SIZE[0] and 0 <= snake.head[1] < WINDOW_SIZE[1]):
                reward = -999
                game_over = True
            
            next_state = get_state(snake, apple)
            ai.update_q_value(state, action, reward, next_state)
            
            if visible:
                screen.fill((0, 0, 0))
                snake.display(screen, PIXEL_SIZE)
                pygame.draw.rect(screen, (255, 0, 0), (*apple, PIXEL_SIZE, PIXEL_SIZE))
                pygame.display.flip()
                clock.tick(10)
            
        total_score += score
        if score > best_score:
            best_score = score
        
        if not episode % 100 and episode:
            print("Game :", episode)
            print("Best score :", best_score)
            print("Average score :", total_score / episode)
        
        if visible:
            print(score)
    
    if not visible:
        ai.save_q_table()
    pygame.quit()

run_game(visible=True, episodes=1)  # See the AI play
# run_game(visible=False, episodes=20000)  # Train fast without display