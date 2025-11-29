import tkinter as tk
from tkinter import ttk, messagebox
import math

# ==================== RED-BLACK TREE ====================
class RBNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.color = 'RED'

class RedBlackTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        node = RBNode(value)
        if not self.root:
            self.root = node
            self.root.color = 'BLACK'
            return
        
        parent = None
        current = self.root
        
        while current:
            parent = current
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return  # Duplicate
        
        node.parent = parent
        if value < parent.value:
            parent.left = node
        else:
            parent.right = node
        
        self._fix_insert(node)
    
    def _fix_insert(self, node):
        while node.parent and node.parent.color == 'RED':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._rotate_left(node.parent.parent)
        self.root.color = 'BLACK'
    
    def _rotate_left(self, node):
        right = node.right
        node.right = right.left
        if right.left:
            right.left.parent = node
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right
        right.left = node
        node.parent = right
    
    def _rotate_right(self, node):
        left = node.left
        node.left = left.right
        if left.right:
            left.right.parent = node
        left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node == node.parent.right:
            node.parent.right = left
        else:
            node.parent.left = left
        left.right = node
        node.parent = left
    
    def search(self, value):
        current = self.root
        while current:
            if value == current.value:
                return current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return None
    
    def delete(self, value):
        node = self.search(value)
        if not node:
            return
        self._delete_node(node)
    
    def _delete_node(self, node):
        y = node
        y_original_color = y.color
        
        if not node.left:
            x = node.right
            self._transplant(node, node.right)
        elif not node.right:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                if x:
                    x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        
        if y_original_color == 'BLACK' and x:
            self._fix_delete(x)
    
    def _minimum(self, node):
        while node.left:
            node = node.left
        return node
    
    def _transplant(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent
    
    def _fix_delete(self, node):
        while node != self.root and node.color == 'BLACK':
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling and sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    node.parent.color = 'RED'
                    self._rotate_left(node.parent)
                    sibling = node.parent.right
                if sibling and (not sibling.left or sibling.left.color == 'BLACK') and \
                   (not sibling.right or sibling.right.color == 'BLACK'):
                    sibling.color = 'RED'
                    node = node.parent
                else:
                    if sibling and (not sibling.right or sibling.right.color == 'BLACK'):
                        if sibling.left:
                            sibling.left.color = 'BLACK'
                        sibling.color = 'RED'
                        self._rotate_right(sibling)
                        sibling = node.parent.right
                    if sibling:
                        sibling.color = node.parent.color
                        node.parent.color = 'BLACK'
                        if sibling.right:
                            sibling.right.color = 'BLACK'
                        self._rotate_left(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling and sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    node.parent.color = 'RED'
                    self._rotate_right(node.parent)
                    sibling = node.parent.left
                if sibling and (not sibling.right or sibling.right.color == 'BLACK') and \
                   (not sibling.left or sibling.left.color == 'BLACK'):
                    sibling.color = 'RED'
                    node = node.parent
                else:
                    if sibling and (not sibling.left or sibling.left.color == 'BLACK'):
                        if sibling.right:
                            sibling.right.color = 'BLACK'
                        sibling.color = 'RED'
                        self._rotate_left(sibling)
                        sibling = node.parent.left
                    if sibling:
                        sibling.color = node.parent.color
                        node.parent.color = 'BLACK'
                        if sibling.left:
                            sibling.left.color = 'BLACK'
                        self._rotate_right(node.parent)
                    node = self.root
        node.color = 'BLACK'

# ==================== 2-3-4 TREE ====================
class Node234:
    def __init__(self):
        self.keys = []
        self.children = []
        self.parent = None
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def is_full(self):
        return len(self.keys) == 3

class Tree234:
    def __init__(self):
        self.root = Node234()
    
    def insert(self, value):
        if self.root.is_full():
            new_root = Node234()
            new_root.children.append(self.root)
            self.root.parent = new_root
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, value)
    
    def _insert_non_full(self, node, value):
        i = len(node.keys) - 1
        
        if node.is_leaf():
            node.keys.append(0)
            while i >= 0 and value < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = value
        else:
            while i >= 0 and value < node.keys[i]:
                i -= 1
            i += 1
            
            if node.children[i].is_full():
                self._split_child(node, i)
                if value > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], value)
    
    def _split_child(self, parent, index):
        full_node = parent.children[index]
        new_node = Node234()
        new_node.parent = parent
        
        mid_key = full_node.keys[1]
        new_node.keys = [full_node.keys[2]]
        full_node.keys = [full_node.keys[0]]
        
        if not full_node.is_leaf():
            new_node.children = [full_node.children[2], full_node.children[3]]
            full_node.children = [full_node.children[0], full_node.children[1]]
            for child in new_node.children:
                child.parent = new_node
        
        parent.keys.insert(index, mid_key)
        parent.children.insert(index + 1, new_node)
    
    def search(self, value, node=None):
        if node is None:
            node = self.root
        
        i = 0
        while i < len(node.keys) and value > node.keys[i]:
            i += 1
        
        if i < len(node.keys) and value == node.keys[i]:
            return node
        if node.is_leaf():
            return None
        return self.search(value, node.children[i])
    
    def delete(self, value):
        if not self.root:
            return
        self._delete_from_node(self.root, value)
        if len(self.root.keys) == 0 and len(self.root.children) > 0:
            self.root = self.root.children[0]
            self.root.parent = None
    
    def _delete_from_node(self, node, value):
        i = 0
        while i < len(node.keys) and value > node.keys[i]:
            i += 1
        
        if i < len(node.keys) and value == node.keys[i]:
            if node.is_leaf():
                node.keys.pop(i)
            else:
                pred = self._get_predecessor(node, i)
                node.keys[i] = pred
                self._delete_from_node(node.children[i], pred)
                self._fix_child(node, i)
        elif not node.is_leaf() and i < len(node.children):
            self._delete_from_node(node.children[i], value)
            self._fix_child(node, i)
    
    def _fix_child(self, parent, index):
        child = parent.children[index]

        if len(child.keys) > 0:
            return

        if index > 0 and len(parent.children[index - 1].keys) > 1:
            left_sibling = parent.children[index - 1]

            child.keys.insert(0, parent.keys[index - 1])

            parent.keys[index - 1] = left_sibling.keys.pop()

            if not left_sibling.is_leaf():
                child.children.insert(0, left_sibling.children.pop())

            return

        if index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > 1:
            right_sibling = parent.children[index + 1]

            child.keys.append(parent.keys[index])

            parent.keys[index] = right_sibling.keys.pop(0)

            if not right_sibling.is_leaf():
                child.children.append(right_sibling.children.pop(0))

            return

        if index > 0:
            # Merge com irmão esquerdo
            left_sibling = parent.children[index - 1]

            left_sibling.keys.append(parent.keys.pop(index - 1))

            left_sibling.keys.extend(child.keys)

            if not child.is_leaf():
                left_sibling.children.extend(child.children)

            parent.children.pop(index)

        else:
            right_sibling = parent.children[index + 1]

            child.keys.append(parent.keys.pop(index))

            child.keys.extend(right_sibling.keys)

            if not right_sibling.is_leaf():
                child.children.extend(right_sibling.children)

            parent.children.pop(index + 1)
    
    def _get_predecessor(self, node, index):
        current = node.children[index]
        while not current.is_leaf():
            current = current.children[-1]
        return current.keys[-1]

# ==================== SPLAY TREE ====================
class SplayNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None
    
    def _right_rotate(self, node):
        left = node.left
        node.left = left.right
        if left.right:
            left.right.parent = node
        left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node == node.parent.right:
            node.parent.right = left
        else:
            node.parent.left = left
        left.right = node
        node.parent = left
    
    def _left_rotate(self, node):
        right = node.right
        node.right = right.left
        if right.left:
            right.left.parent = node
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right
        right.left = node
        node.parent = right
    
    def _splay(self, node):
        while node.parent:
            if not node.parent.parent:
                if node == node.parent.left:
                    self._right_rotate(node.parent)
                else:
                    self._left_rotate(node.parent)
            elif node == node.parent.left and node.parent == node.parent.parent.left:
                self._right_rotate(node.parent.parent)
                self._right_rotate(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.right:
                self._left_rotate(node.parent.parent)
                self._left_rotate(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.left:
                self._left_rotate(node.parent)
                self._right_rotate(node.parent)
            else:
                self._right_rotate(node.parent)
                self._left_rotate(node.parent)
    
    def insert(self, value):
        node = SplayNode(value)
        if not self.root:
            self.root = node
            return
        
        current = self.root
        parent = None
        
        while current:
            parent = current
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return
        
        node.parent = parent
        if value < parent.value:
            parent.left = node
        else:
            parent.right = node
        
        self._splay(node)
    
    def search(self, value):
        current = self.root
        last = None
        
        while current:
            last = current
            if value == current.value:
                self._splay(current)
                return current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        
        if last:
            self._splay(last)
        return None
    
    def delete(self, value):
        node = self.search(value)
        if not node:
            return
        
        self._splay(node)
        
        if not node.left:
            self.root = node.right
            if self.root:
                self.root.parent = None
        elif not node.right:
            self.root = node.left
            if self.root:
                self.root.parent = None
        else:
            left_max = self._find_max(node.left)
            self._splay(left_max)
            left_max.right = node.right
            if node.right:
                node.right.parent = left_max
            self.root = left_max
            self.root.parent = None
    
    def _find_max(self, node):
        while node.right:
            node = node.right
        return node

# ==================== GUI ====================
class TreeVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Árvores Balanceadas")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1e293b')
        
        self.tree_type = tk.StringVar(value='redblack')
        self.tree = None
        self.found_node = None
        
        self._create_widgets()
        self._initialize_tree()
    
    def _create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Visualizador de Árvores Balanceadas", 
                        font=('Arial', 24, 'bold'), bg='#1e293b', fg='white')
        title.pack(pady=20)
        
        # Tree type selection
        type_frame = tk.Frame(self.root, bg='#334155', relief=tk.RAISED, bd=2)
        type_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(type_frame, text="Tipo de Árvore:", font=('Arial', 12, 'bold'),
                bg='#334155', fg='white').pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Radiobutton(type_frame, text="Red-Black Tree", variable=self.tree_type,
                      value='redblack', command=self._initialize_tree, font=('Arial', 11),
                      bg='#334155', fg='white', selectcolor='#ef4444',
                      activebackground='#334155', activeforeground='white').pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(type_frame, text="Árvore 2-3-4", variable=self.tree_type,
                      value='234', command=self._initialize_tree, font=('Arial', 11),
                      bg='#334155', fg='white', selectcolor='#3b82f6',
                      activebackground='#334155', activeforeground='white').pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(type_frame, text="Splay Tree", variable=self.tree_type,
                      value='splay', command=self._initialize_tree, font=('Arial', 11),
                      bg='#334155', fg='white', selectcolor='#10b981',
                      activebackground='#334155', activeforeground='white').pack(side=tk.LEFT, padx=5)
        
        # Controls
        control_frame = tk.Frame(self.root, bg='#334155', relief=tk.RAISED, bd=2)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(control_frame, text="Valor:", font=('Arial', 12, 'bold'),
                bg='#334155', fg='white').pack(side=tk.LEFT, padx=10, pady=10)
        
        self.value_entry = tk.Entry(control_frame, font=('Arial', 12), width=10)
        self.value_entry.pack(side=tk.LEFT, padx=5)
        self.value_entry.bind('<Return>', lambda e: self._insert())
        
        tk.Button(control_frame, text="Inserir", command=self._insert,
                 bg='#10b981', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Remover", command=self._delete,
                 bg='#ef4444', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Buscar", command=self._search,
                 bg='#3b82f6', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Limpar", command=self._initialize_tree,
                 bg='#64748b', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Message
        self.message_var = tk.StringVar(value="Árvore inicializada")
        message_label = tk.Label(self.root, textvariable=self.message_var,
                                font=('Arial', 11), bg='#475569', fg='white',
                                relief=tk.RAISED, bd=2)
        message_label.pack(pady=5, padx=20, fill=tk.X)
        
        # Canvas
        canvas_frame = tk.Frame(self.root, bg='white', relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Legend
        legend_frame = tk.Frame(self.root, bg='#334155', relief=tk.RAISED, bd=2)
        legend_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(legend_frame, text="Legenda:", font=('Arial', 11, 'bold'),
                bg='#334155', fg='white').pack(side=tk.LEFT, padx=10)
        
        self.legend_label = tk.Label(legend_frame, font=('Arial', 10),
                                     bg='#334155', fg='#cbd5e1')
        self.legend_label.pack(side=tk.LEFT, padx=10)
        self._update_legend()
    
    def _update_legend(self):
        tree_type = self.tree_type.get()
        if tree_type == 'redblack':
            self.legend_label.config(text="🔴 Nó Vermelho  ⚫ Nó Preto")
        elif tree_type == '234':
            self.legend_label.config(text="Cada caixa pode conter 1, 2 ou 3 chaves")
        else:
            self.legend_label.config(text="O nó acessado mais recentemente é movido para a raiz")
    
    def _initialize_tree(self):
        tree_type = self.tree_type.get()
        if tree_type == 'redblack':
            self.tree = RedBlackTree()
        elif tree_type == '234':
            self.tree = Tree234()
        else:
            self.tree = SplayTree()
        
        self.found_node = None
        self.message_var.set("Árvore inicializada")
        self._update_legend()
        self._draw_tree()
    
    def _insert(self):
        try:
            value = int(self.value_entry.get())
            self.tree.insert(value)
            self.found_node = None
            self.message_var.set(f"Valor {value} inserido e árvore balanceada")
            self.value_entry.delete(0, tk.END)
            self._draw_tree()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido")
    
    def _delete(self):
        try:
            value = int(self.value_entry.get())
            self.tree.delete(value)
            self.found_node = None
            self.message_var.set(f"Valor {value} removido e árvore balanceada")
            self.value_entry.delete(0, tk.END)
            self._draw_tree()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido")
    
    def _search(self):
        try:
            value = int(self.value_entry.get())
            result = self.tree.search(value)
            if result:
                self.found_node = result
                self.message_var.set(f"Valor {value} encontrado na árvore!")
            else:
                self.found_node = None
                self.message_var.set(f"Valor {value} não encontrado na árvore")
            self._draw_tree()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido")
    
    def _draw_tree(self):
        self.canvas.delete("all")
        
        if not self.tree.root:
            return
        
        width = self.canvas.winfo_width() or 1100
        height = self.canvas.winfo_height() or 500
        
        if self.tree_type.get() == '234':
            self._draw_234_tree(self.tree.root, width // 2, 40, width // 4)
        else:
            self._draw_binary_tree(self.tree.root, width // 2, 40, width // 4)
    
    def _draw_binary_tree(self, node, x, y, offset):
        if not node:
            return
        
        # Draw connections
        if node.left:
            self.canvas.create_line(x, y, x - offset, y + 80, fill='#64748b', width=2)
            self._draw_binary_tree(node.left, x - offset, y + 80, offset / 2)
        
        if node.right:
            self.canvas.create_line(x, y, x + offset, y + 80, fill='#64748b', width=2)
            self._draw_binary_tree(node.right, x + offset, y + 80, offset / 2)
        
        # Draw node - check if it's Red-Black Tree or Splay Tree
        if hasattr(node, 'color'):
            color = '#ef4444' if node.color == 'RED' else '#1e293b'
        else:
            color = '#10b981'  # Green for Splay Tree
        
        # Highlight if found
        if node == self.found_node:
            self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, 
                                   fill='#fbbf24', outline='#f59e0b', width=3)
        
        self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, 
                               fill=color, outline='#475569', width=2)
        self.canvas.create_text(x, y, text=str(node.value), 
                               fill='white', font=('Arial', 12, 'bold'))
    
    def _draw_234_tree(self, node, x, y, offset):
        if not node or len(node.keys) == 0:
            return
        
        node_width = 40 * len(node.keys)
        
        # Draw connections to children
        if len(node.children) > 0:
            child_spacing = offset * 2 / (len(node.children) + 1)
            for i, child in enumerate(node.children):
                child_x = x - offset + child_spacing * (i + 1)
                self.canvas.create_line(x, y + 20, child_x, y + 80, 
                                       fill='#64748b', width=2)
                self._draw_234_tree(child, child_x, y + 80, offset / 2)
        
        # Highlight if found
        if node == self.found_node:
            self.canvas.create_rectangle(x - node_width // 2 - 5, y - 25,
                                        x + node_width // 2 + 5, y + 25,
                                        fill='#fbbf24', outline='#f59e0b', width=3)
        
        # Draw node
        self.canvas.create_rectangle(x - node_width // 2, y - 20,
                                    x + node_width // 2, y + 20,
                                    fill='#1e293b', outline='#64748b', width=2)
        
        # Draw keys
        for i, key in enumerate(node.keys):
            key_x = x - node_width // 2 + 20 + i * 40
            self.canvas.create_text(key_x, y, text=str(key),
                                   fill='white', font=('Arial', 12, 'bold'))

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeVisualizerApp(root)
    root.mainloop()