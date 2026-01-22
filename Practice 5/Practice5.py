from PIL import Image, ImageDraw
import sys

INPUT_FILE = 'init01.csv'
OUTPUT_FILE_CSV = 'generation.csv'
OUTPUT_FILE_PNG = 'generation.png'
GENERATIONS = 10
DEBUG = True
CELL_SIZE = 15
BORDER_WIDTH = 2
BASE_COLOR = (0, 255, 0)  



def live_neighbors(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])
    min_r = max(0, row - 1)
    max_r = min(rows - 1, row + 1)
    min_c = max(0, col - 1)
    max_c = min(cols - 1, col + 1)
    count = 0
    for idx_y in range(min_r, max_r + 1):
        for idx_x in range(min_c, max_c + 1):
            if idx_y == row and idx_x == col:
                continue
            if grid[idx_y][idx_x] == 1:
                count += 1
    return count

def make_zeros_matrix(grid,age_of_cell):
    rows, cols = len(grid), len(grid[0])
    lil_mass = []
    for row in range(rows):
        for col in range(cols):
            lil_mass.append(0)
        age_of_cell.append(lil_mass)
    return(age_of_cell)

def model_of_life(grid,age_of_cell):


    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1:
                age_of_cell[row][col] = 1

    for row in range(rows):
        for col in range(cols):
            live_nb = live_neighbors(grid, row, col)

            # Правило смерти без популяции
            if grid[row][col] == 1 and live_nb < 2:
                new_grid[row][col] = 0
                age_of_cell[row][col] = 0

            # Правило выживания с популяцией
            elif grid[row][col] == 1 and (live_nb == 2 or live_nb == 3):
                new_grid[row][col] = 1
                age_of_cell[row][col] += 1

            # Правило вымирания при большой популяции
            elif grid[row][col] == 1 and live_nb > 3:
                new_grid[row][col] = 0
                age_of_cell[row][col] = 0

            # Правило рождения
            elif grid[row][col] == 0 and live_nb == 3:
                new_grid[row][col] = 1
                age_of_cell[row][col] = 1

            else:
                new_grid[row][col] = 0
                age_of_cell[row][col] = 0

    return new_grid,age_of_cell


def read_input(filename):
    grid = []
    with open(filename, "r") as input_file:
        lines = input_file.readlines()
        if DEBUG:
            print(f"File contents: {lines}")

        for line in lines:
            cells = line.split(',')
            cells = [[int(numb) for numb in cells]]

            if cells: 
                grid.append(cells[0])

    if grid:
        first_stroke_len = len(grid[0])
        for i, row in enumerate(grid):
            if len(row) != first_stroke_len:
                print(f"Warning: Row {i} has different length ({len(row)} vs {first_stroke_len})")

    return grid


def write_output(grid, filename, generation_num):
    with open(f"{generation_num}_{filename}", "w") as output_file:
        for row in grid:
            line = ','.join(str(cell) for cell in row)
            output_file.write(line + '\n')


def write_png(grid, filename, generation_num,age_of_cells, base_color=BASE_COLOR):
    rows = len(grid)
    cols = len(grid[0])

    width_image = cols * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
    height_image = rows * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH

    image = Image.new('RGB', (width_image, height_image), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)

    

    for row in range(rows):
        for col in range(cols):
            x1 = col * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
            y1 = row * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            if grid[row][col] == 1:
                age = age_of_cells[row][col]
                factor_of_dying = min(0.4 + (age * 0.1), 0.95)  
                color = tuple(int(c * factor_of_dying) for c in base_color)
                draw.rectangle([x1, y1, x2, y2], fill=color, outline=(0, 0, 0))
            else:
                draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255), outline=(0, 0, 0))

    for i in range(cols + 1):
        x = i * (CELL_SIZE + BORDER_WIDTH)
        draw.line([(x, 0), (x, height_image)], fill=(0, 0, 255), width=BORDER_WIDTH)

    for i in range(rows + 1):
        y = i * (CELL_SIZE + BORDER_WIDTH)
        draw.line([(0, y), (width_image, y)], fill=(0, 0, 255), width=BORDER_WIDTH)

    # Изображение в файл
    output_filename = f"{generation_num}_{filename}"
    image.save(output_filename)

    if DEBUG:
        print(f"Image saved as {output_filename}")


def main():
    age_of_cells = []

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = INPUT_FILE

    if len(sys.argv) > 2:
        try:
            generations = int(sys.argv[2])
        except ValueError:
            print(f"Invalid generations value: {sys.argv[2]}, using default: {GENERATIONS}")
            generations = GENERATIONS
    else:
        generations = GENERATIONS

    if len(sys.argv) > 3:
        try:
            color_parts = sys.argv[3].split(',')

            if len(color_parts) == 3:
                base_color = tuple(int(c) for c in color_parts)
            else:
                raise ValueError

        except (ValueError, IndexError):
            print(f"Invalid color format: {sys.argv[3]}, using default: {BASE_COLOR}")
            base_color = BASE_COLOR
    else:
        base_color = BASE_COLOR

    grid = read_input(input_file)
    if not grid:
        print("Error: Empty grid or invalid input file")
        return

    if DEBUG:
        print(f"Initial grid ({len(grid)}x{len(grid[0])}):")
        for row in grid:
            print(row)
        print(f"\nSimulating {generations} generations...\n")

    make_zeros_matrix(grid,age_of_cells)
    for generation in range(1, generations + 1):
        grid,age_of_cells = model_of_life(grid,age_of_cells)

        write_output(grid, OUTPUT_FILE_CSV, generation)
        write_png(grid, OUTPUT_FILE_PNG, generation,age_of_cells, base_color)

        if DEBUG:
            print(f"Generation {generation} completed")
            alive_count = sum(sum(row) for row in grid)
            print(f"  Alive cells: {alive_count}")

    if DEBUG:
        print(f"\nSimulation completed. Results saved with prefixes 0-{generations}.")


main()

