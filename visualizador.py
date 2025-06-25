import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
from scipy.fft import fft
from scipy.signal import tf2zpk
from PIL import Image, ImageTk
import webbrowser
import os

class CalculusIVVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Calc4Visualgo")
        self.root.geometry("1000x800")
        
        
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=10)
        self.style.configure('TButton', padding=5)
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 12))
        self.style.configure('Names.TLabel', font=('Arial', 10))
        self.logo_image = self.load_image("", (300, 150))
        
        self.setup_main_menu()
    
    def load_image(self, filename, size):
        """Carrega e redimensiona uma imagem."""
        try:
            img_path = os.path.join(os.path.dirname(__file__), filename)
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            return None
    
    def setup_main_menu(self):
        """Menu inicial personalizado."""
        self.clear_frame()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
  
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        if self.logo_image:
            logo_label = ttk.Label(header_frame, image=self.logo_image)
            logo_label.pack(side=tk.LEFT, padx=20)
        
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, expand=True)
        
        ttk.Label(
            title_frame, 
            text="Calc4Visualgo", 
            style='Title.TLabel'
        ).pack(pady=5)
        
        ttk.Label(
            title_frame, 
            text="Ferramenta de Visualização Matemática",
            style='Subtitle.TLabel'
        ).pack()
        
       
        authors_frame = ttk.Frame(title_frame)
        authors_frame.pack(pady=10)
        
        ttk.Label(
            authors_frame, 
            text="Desenvolvido por:",
            style='Names.TLabel'
        ).pack()
        
        ttk.Label(
            authors_frame, 
            text=" Henrique Acacio de Souza Farias - Luiz Afonso Camilotti Justo",
            style='Names.TLabel'
        ).pack()
        
        ttk.Label(
            authors_frame, 
            text="Universidade Técnológica Federal do Paraná - Campus Toledo - Curso de Graduação em Engenharia de Computação",
            style='Names.TLabel'
        ).pack(pady=10)
  
        topics_frame = ttk.Frame(main_frame)
        topics_frame.pack(pady=20)
        
        topics = [
            ("Séries de Fourier", "fourier_series"),
            ("Transformada de Fourier", "fourier_transform"),
            ("Transformada de Laplace", "laplace_transform"),
            ("Transformada Z", "z_transform")
        ]
        
        for text, topic in topics:
            btn = ttk.Button(
                topics_frame, 
                text=text, 
                width=30,
                command=lambda t=topic: self.show_topic_interface(t)
            )
            btn.pack(pady=5)

        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        ttk.Button(
            footer_frame, 
            text="Sobre", 
            command=self.show_about
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            footer_frame, 
            text="Repositório", 
            command=lambda: webbrowser.open("https://github.com/HenFarias/Visualizador_Serie_Fourier")
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            footer_frame, 
            text="Sair", 
            command=self.root.quit
        ).pack(side=tk.RIGHT, padx=10)
    
    def show_about(self):
        """Janela 'Sobre' com informações do projeto."""
        about_window = tk.Toplevel(self.root)
        about_window.title("Sobre o Visualizador")
        about_window.geometry("600x400")
        
        main_frame = ttk.Frame(about_window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(
            main_frame, 
            text="Calc4Visualgo", 
            style='Title.TLabel'
        ).pack(pady=10)
        
        about_text = """
O software 'Calc4Visualgo' foi desenvolvido como parte do trabalho de Cálculo 4.

Tendo como objetivo:
- Visualizar conceitos matemáticos avançados de forma didática
- Facilitar o aprendizado de transformadas integrais
- Demonstrar aplicações práticas


Desenvolvido por:
Henrique Acacio de Souza Farias
Luiz Afonso Camilotti Justo

Disciplina: Cálculo 4
Profª Karen Carrilho

Universidade Tecnológica Federal do Paraná - Campus Toledo
2025
"""
        ttk.Label(
            main_frame, 
            text=about_text,
            justify=tk.LEFT
        ).pack(fill=tk.X, pady=10)
        
        repo_frame = ttk.Frame(main_frame)
        repo_frame.pack(pady=10)
        
        ttk.Label(
            repo_frame, 
            text="Código disponível em:"
        ).pack(side=tk.LEFT)
        
        repo_link = ttk.Label(
            repo_frame, 
            text="https://github.com/HenFarias/Visualizador_Serie_Fourier",
            foreground="blue",
            cursor="hand2"
        )
        repo_link.pack(side=tk.LEFT)
        repo_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/HenFarias/Visualizador_Serie_Fourier"))
        
        close_btn = ttk.Button(
            main_frame, 
            text="Fechar", 
            command=about_window.destroy
        )
        close_btn.pack(pady=10)
    
    def show_topic_interface(self, topic):
        """Carrega a interface do tópico selecionado."""
        self.clear_frame()
        

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
 
      
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
       
        back_btn = ttk.Button(
            control_frame, 
            text="← Voltar ao Menu", 
            command=self.setup_main_menu
        )
        back_btn.pack(side=tk.LEFT, padx=5)
        
        # Configura a interface específica
        if topic == "fourier_series":
            self.setup_fourier_series(control_frame, main_frame)
        elif topic == "fourier_transform":
            self.setup_fourier_transform(control_frame, main_frame)
        elif topic == "laplace_transform":
            self.setup_laplace_transform(control_frame, main_frame)
        elif topic == "z_transform":
            self.setup_z_transform(control_frame, main_frame)
    
    def setup_fourier_series(self, control_frame, main_frame):
        """Interface para Séries de Fourier."""

        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(side=tk.LEFT, padx=10)
        

        ttk.Label(settings_frame, text="Tipo de Onda:").grid(row=0, column=0, sticky=tk.W)
        self.wave_type = ttk.Combobox(
            settings_frame, 
            values=["quadrada", "triangular", "dente de serra"],
            state="readonly"
        )
        self.wave_type.current(0)
        self.wave_type.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(settings_frame, text="Nº de Termos:").grid(row=1, column=0, sticky=tk.W)
        self.n_terms = tk.IntVar(value=5)
        terms_slider = ttk.Scale(
            settings_frame, 
            from_=1, 
            to=50, 
            variable=self.n_terms,
            orient="horizontal"
        )
        terms_slider.grid(row=1, column=1, padx=5, pady=2)
        

        self.show_individual = tk.BooleanVar(value=False)
        individual_check = ttk.Checkbutton(
            settings_frame, 
            text="Mostrar Harmônicos Individuais",
            variable=self.show_individual
        )
        individual_check.grid(row=2, columnspan=2, pady=5)
        
        plot_btn = ttk.Button(
            control_frame, 
            text="Plotar", 
            command=self.plot_fourier_series
        )
        plot_btn.pack(side=tk.RIGHT, padx=5)
        

        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    
        self.plot_fourier_series()
    
    def plot_fourier_series(self):
        """Plot da Série de Fourier."""
        try:
            x = np.linspace(0, 4 * np.pi, 1000)
            n_terms = self.n_terms.get()
            wave_type = self.wave_type.get()
            
            y, harmonics = self.calculate_fourier_series(x, n_terms, wave_type)
            
            self.ax.clear()
            self.ax.plot(x, y, 'r-', linewidth=2, label=f"Aproximação ({n_terms} termos)")
            
            if self.show_individual.get():
                for i, harmonic in enumerate(harmonics):
                    self.ax.plot(x, harmonic, '--', alpha=0.3, label=f"Harmônico {i+1}")
            
            self.ax.set_title(f"Série de Fourier: Onda {wave_type.capitalize()}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("f(x)")
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.legend()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")
    
    def calculate_fourier_series(self, x, n_terms, wave_type):
        """Calcula a Série de Fourier."""
        result = np.zeros_like(x)
        harmonics = []
        
        if wave_type == "quadrada":
            for n in range(1, n_terms + 1):
                harmonic = (4 / (np.pi * (2*n - 1))) * np.sin((2*n - 1) * x)
                harmonics.append(harmonic)
                result += harmonic
        elif wave_type == "triangular":
            for n in range(1, n_terms + 1):
                harmonic = ((-1)**(n-1)) * (8 / (np.pi**2 * (2*n - 1)**2)) * np.sin((2*n - 1) * x)
                harmonics.append(harmonic)
                result += harmonic
        elif wave_type == "dente de serra":
            for n in range(1, n_terms + 1):
                harmonic = (2 / (np.pi * n)) * ((-1)**(n+1)) * np.sin(n * x)
                harmonics.append(harmonic)
                result += harmonic
        
        return result, harmonics
    
    def setup_fourier_transform(self, control_frame, main_frame):
        """Interface para Transformada de Fourier."""
        
        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(settings_frame, text="Expressão do sinal:").grid(row=0, column=0, sticky=tk.W)
        self.signal_input = ttk.Entry(settings_frame, width=25)
        self.signal_input.insert(0, "np.sin(2*np.pi*5*x)")
        self.signal_input.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(settings_frame, text="Freq. amostragem (Hz):").grid(row=1, column=0, sticky=tk.W)
        self.sample_freq = tk.IntVar(value=1000)
        ttk.Entry(settings_frame, textvariable=self.sample_freq, width=10).grid(row=1, column=1, padx=5, pady=2)
        

        plot_btn = ttk.Button(
            control_frame, 
            text="Calcular FFT", 
            command=self.plot_fft
        )
        plot_btn.pack(side=tk.RIGHT, padx=5)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.plot_fft()
    
    def plot_fft(self):
        """Plot da Transformada de Fourier (FFT)."""
        try:
            fs = self.sample_freq.get()
            t = np.linspace(0, 1, fs, endpoint=False)
            
            namespace = {
                'np': np,
                'sin': np.sin,
                'cos': np.cos,
                'exp': np.exp,
                'pi': np.pi,
                't': t,
                'x': t
            }
            
          
            signal = eval(self.signal_input.get(), namespace)
            
    
            n = len(signal)
            freq = np.fft.fftfreq(n, 1/fs)[:n//2]
            fft_values = np.abs(fft(signal))[:n//2]
            
        
            self.ax1.clear()
            self.ax1.plot(t, signal, 'b-')
            self.ax1.set_title("Sinal no Domínio do Tempo")
            self.ax1.set_xlabel("Tempo (s)")
            self.ax1.set_ylabel("Amplitude")
            self.ax1.grid(True, linestyle='--', alpha=0.6)
            

            self.ax2.clear()
            self.ax2.stem(freq, fft_values, 'r-', markerfmt=" ", basefmt="-r")
            self.ax2.set_title("Transformada de Fourier (FFT)")
            self.ax2.set_xlabel("Frequência (Hz)")
            self.ax2.set_ylabel("Magnitude")
            self.ax2.grid(True, linestyle='--', alpha=0.6)
            
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Expressão inválida ou erro no cálculo:\n{str(e)}")
    
    def setup_laplace_transform(self, control_frame, main_frame):
        """Interface para Transformada de Laplace."""

        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(settings_frame, text="Função no tempo:").grid(row=0, column=0, sticky=tk.W)
        self.laplace_input = ttk.Entry(settings_frame, width=25)
        self.laplace_input.insert(0, "np.exp(-2*t)*np.sin(2*np.pi*3*t)")
        self.laplace_input.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(settings_frame, text="Tempo máximo (s):").grid(row=1, column=0, sticky=tk.W)
        self.time_max = tk.DoubleVar(value=5.0)
        ttk.Entry(settings_frame, textvariable=self.time_max, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        plot_btn = ttk.Button(
            control_frame, 
            text="Calcular Transformada", 
            command=self.plot_laplace
        )
        plot_btn.pack(side=tk.RIGHT, padx=5)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.plot_laplace()
    
    def plot_laplace(self):
        """Plot da Transformada de Laplace (simulação numérica)."""
        try:
            t_max = self.time_max.get()
            t = np.linspace(0, t_max, 1000)
            
            namespace = {
                'np': np,
                'sin': np.sin,
                'cos': np.cos,
                'exp': np.exp,
                'pi': np.pi,
                't': t
            }
            
            time_func = eval(self.laplace_input.get(), namespace)
            
            sigma = np.linspace(0.1, 10, 100)
            omega = np.linspace(-20, 20, 100)
            s = sigma[:, None] + 1j * omega
            
            laplace = np.array([
                np.trapz(time_func * np.exp(-s_i * t), t) 
                for s_i in s.ravel()
            ]).reshape(s.shape)
            
        
            self.ax1.clear()
            self.ax1.plot(t, time_func, 'g-')
            self.ax1.set_title("Função no Domínio do Tempo")
            self.ax1.set_xlabel("Tempo (s)")
            self.ax1.set_ylabel("Amplitude")
            self.ax1.grid(True, linestyle='--', alpha=0.6)
            
            self.ax2.clear()
            magnitude = np.abs(laplace)
            X, Y = np.meshgrid(omega, sigma)
            contour = self.ax2.contourf(X, Y, magnitude, levels=20, cmap='viridis')
            self.fig.colorbar(contour, ax=self.ax2, label='Magnitude')
            self.ax2.set_title("Magnitude da Transformada de Laplace")
            self.ax2.set_xlabel("Frequência (ω)")
            self.ax2.set_ylabel("σ")
            
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Expressão inválida ou erro no cálculo:\n{str(e)}")
    
    def setup_z_transform(self, control_frame, main_frame):
        """Interface para Transformada Z."""

        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(side=tk.LEFT, padx=10)
        

        ttk.Label(settings_frame, text="Coeficientes do numerador:").grid(row=0, column=0, sticky=tk.W)
        self.num_input = ttk.Entry(settings_frame, width=25)
        self.num_input.insert(0, "[1, -0.5]")
        self.num_input.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(settings_frame, text="Coeficientes do denominador:").grid(row=1, column=0, sticky=tk.W)
        self.den_input = ttk.Entry(settings_frame, width=25)
        self.den_input.insert(0, "[1, -0.8]")
        self.den_input.grid(row=1, column=1, padx=5, pady=2)
        

        plot_btn = ttk.Button(
            control_frame, 
            text="Plotar Polos e Zeros", 
            command=self.plot_z_transform
        )
        plot_btn.pack(side=tk.RIGHT, padx=5)

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.plot_z_transform()
    
    def plot_z_transform(self):
        """Plot da Transformada Z (Diagrama de Polos e Zeros)."""
        try:
           
            num = eval(self.num_input.get())
            den = eval(self.den_input.get())
            
         
            zeros, poles, _ = tf2zpk(num, den)
            
            self.ax.clear()
            
   
            self.ax.scatter(
                np.real(zeros), 
                np.imag(zeros), 
                marker='o', 
                color='b', 
                s=100, 
                label="Zeros"
            )
            
        
            self.ax.scatter(
                np.real(poles), 
                np.imag(poles), 
                marker='x', 
                color='r', 
                s=100, 
                label="Polos"
            )
            
            unit_circle = plt.Circle(
                (0, 0), 
                1, 
                fill=False, 
                linestyle='--', 
                color='gray', 
                alpha=0.5
            )
            self.ax.add_patch(unit_circle)
            
            self.ax.set_title("Diagrama de Polos e Zeros (Transformada Z)")
            self.ax.set_xlabel("Parte Real")
            self.ax.set_ylabel("Parte Imaginária")
            self.ax.legend()
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.axis('equal')
            self.ax.set_xlim(-1.5, 1.5)
            self.ax.set_ylim(-1.5, 1.5)
            
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Entrada inválida ou erro no cálculo:\n{str(e)}")
    
    def clear_frame(self):
        """Limpa todos os widgets da janela."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculusIVVisualizer(root)
    root.mainloop()
