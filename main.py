import streamlit as st
import random

# ---------------- INIT ---------------- #
def init_game():
    if "grid" not in st.session_state:
        st.session_state.grid = [[0]*4 for _ in range(4)]
        st.session_state.score = 0
        add_random()
        add_random()

# ---------------- FUNCTIONS ---------------- #
def add_random():
    empty = [(i, j) for i in range(4) for j in range(4) if st.session_state.grid[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        st.session_state.grid[i][j] = 2

def compress(row):
    new = [i for i in row if i != 0]
    new += [0] * (4 - len(new))
    return new

def merge(row):
    for i in range(3):
        if row[i] == row[i+1] and row[i] != 0:
            row[i] *= 2
            st.session_state.score += row[i]
            row[i+1] = 0
    return row

def move_left():
    new_grid = []
    moved = False
    for row in st.session_state.grid:
        compressed = compress(row)
        merged = merge(compressed)
        final = compress(merged)
        if final != row:
            moved = True
        new_grid.append(final)
    st.session_state.grid = new_grid
    return moved

def reverse(grid):
    return [row[::-1] for row in grid]

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def move_right():
    st.session_state.grid = reverse(st.session_state.grid)
    moved = move_left()
    st.session_state.grid = reverse(st.session_state.grid)
    return moved

def move_up():
    st.session_state.grid = transpose(st.session_state.grid)
    moved = move_left()
    st.session_state.grid = transpose(st.session_state.grid)
    return moved

def move_down():
    st.session_state.grid = transpose(st.session_state.grid)
    moved = move_right()
    st.session_state.grid = transpose(st.session_state.grid)
    return moved

def check_win():
    for row in st.session_state.grid:
        if 2048 in row:
            return True
    return False

def check_game_over():
    for row in st.session_state.grid:
        if 0 in row:
            return False
    for i in range(4):
        for j in range(3):
            if st.session_state.grid[i][j] == st.session_state.grid[i][j+1]:
                return False
    for j in range(4):
        for i in range(3):
            if st.session_state.grid[i][j] == st.session_state.grid[i+1][j]:
                return False
    return True

# ---------------- UI ---------------- #
st.title("🎮 2048 Game")
st.markdown("### 👨‍💻 Project Created by **Himanshu Shah**")

init_game()

# Display Score
st.subheader(f"Score: {st.session_state.score}")

# Display Grid
for row in st.session_state.grid:
    cols = st.columns(4)
    for i in range(4):
        value = row[i] if row[i] != 0 else ""
        cols[i].markdown(f"<h3 style='text-align:center'>{value}</h3>", unsafe_allow_html=True)

st.write("")

# Controls
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️ Up"):
        if move_up():
            add_random()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Left"):
        if move_left():
            add_random()

with col3:
    if st.button("➡️ Right"):
        if move_right():
            add_random()

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬇️ Down"):
        if move_down():
            add_random()

# Game Status
if check_win():
    st.success("🎉 You Win!")
elif check_game_over():
    st.error("💀 Game Over!")

# Restart Button
if st.button("🔄 Restart Game"):
    st.session_state.clear()
    st.rerun()

# Footer
st.markdown("---")
st.markdown("<center>👨‍💻 Project Created by <b>Himanshu Shah</b></center>", unsafe_allow_html=True)
