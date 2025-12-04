# Random Quote Generator (Python + MySQL)

A simple Python GUI app built using **Tkinter** that shows a random quote every time you press a button.  
The quotes are stored in a **MySQL database** (using XAMPP).

---

## Features
- Simple Tkinter GUI  
- Shows a random quote  
- Quotes stored in MySQL database  
- Easy to add new quotes  
- Beginner-friendly project

---

## Requirements
- Python 3  
- Tkinter  
- MySQL (XAMPP)  
- mysql-connector-python
  
---

## Database Setup

### 1. Create a database:
```sql
CREATE DATABASE Quote_App;
USE Quote_App;
```

### 2. Create the quotes table:
```sql
CREATE TABLE quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author VARCHAR(100),
    quote TEXT
);
```

### 3. Insert some sample quotes:
```sql
INSERT INTO quotes (author, quote) VALUES
('Steve Jobs', 'The only way to do great work is to love what you do.'),
('Sam Levenson', 'Don’t watch the clock; do what it does. Keep going.'),
('Confucius', 'It does not matter how slowly you go as long as you do not stop.'),
('Dan Reeves', 'Don’t limit your challenges. Challenge your limits.'),
('John C. Maxwell', 'Sometimes you win, sometimes you learn.'),
```

---

## Run the App
```bash
python quote_app.py
```
