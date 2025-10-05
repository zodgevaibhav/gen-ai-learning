import torch
import matplotlib.pyplot as plt
import time
import numpy as np
from matplotlib.animation import FuncAnimation

class CPUvsGPUDemo:
    def __init__(self):
        # Check for available accelerators
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.accelerator_name = "GPU"
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
            self.accelerator_name = "MPS"
        else:
            self.device = torch.device("cpu")
            self.accelerator_name = "CPU"
        
        self.current_device = "CPU"
        self.matrix_size = 1000
        self.history = {'time': [], 'device': [], 'size': [], 'speedup': []}
        self.colors = {'CPU': 'red', 'GPU': 'green', 'MPS': 'blue'}
        
        # Setup plot
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(14, 6))
        self.fig.suptitle('CPU vs GPU Performance Demo', fontsize=16, fontweight='bold')
        
        # Instructions
        self.fig.text(0.5, 0.02, 
                     'Press [D] to switch Device | Press [+] to increase workload | Press [-] to decrease workload',
                     ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        self.setup_plots()
        
    def setup_plots(self):
        # Left plot: Computation time scatter
        self.ax1.set_xlabel('Computation Number', fontsize=12)
        self.ax1.set_ylabel('Time (seconds)', fontsize=12)
        self.ax1.set_title('Computation Time Over Runs', fontsize=13)
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_ylim(0, 1)
        
        # Right plot: Speedup comparison
        self.ax2.set_xlabel('Matrix Size', fontsize=12)
        self.ax2.set_ylabel('Computation Time (seconds)', fontsize=12)
        self.ax2.set_title('CPU vs GPU Performance', fontsize=13)
        self.ax2.grid(True, alpha=0.3)
        
        # Device info text
        accelerator_available = "✓ Available" if self.device.type != "cpu" else "✗ Not Available"
        device_name = ""
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
        elif torch.backends.mps.is_available():
            device_name = "Apple Silicon (MPS)"
        else:
            device_name = "N/A"
        
        self.device_text = self.fig.text(0.02, 0.95, 
                                         f'Current: {self.current_device}\n'
                                         f'Matrix Size: {self.matrix_size}x{self.matrix_size}\n'
                                         f'Accelerator: {accelerator_available}\n'
                                         f'Device: {device_name}',
                                         fontsize=10, verticalalignment='top',
                                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
    def matrix_multiply(self, size, device_type):
        """Perform matrix multiplication on specified device"""
        if device_type == "CPU":
            device = torch.device("cpu")
        elif device_type == "MPS":
            device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
        else:  # GPU
            device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        
        # Create random matrices
        A = torch.randn(size, size, device=device)
        B = torch.randn(size, size, device=device)
        
        # Warm up (especially important for GPU/MPS)
        _ = torch.matmul(A, B)
        if device.type == "cuda":
            torch.cuda.synchronize()
        elif device.type == "mps":
            torch.mps.synchronize()
        
        # Actual timed computation
        start = time.time()
        C = torch.matmul(A, B)
        
        # Ensure accelerator operations are complete
        if device.type == "cuda":
            torch.cuda.synchronize()
        elif device.type == "mps":
            torch.mps.synchronize()
        
        end = time.time()
        elapsed = end - start
        
        return elapsed
    
    def run_computation(self):
        """Run one computation and update history"""
        elapsed = self.matrix_multiply(self.matrix_size, self.current_device)
        
        self.history['time'].append(elapsed)
        self.history['device'].append(self.current_device)
        self.history['size'].append(self.matrix_size)
        
        # Calculate speedup if we have both CPU and accelerator data for same size
        cpu_times = [t for t, d, s in zip(self.history['time'], 
                                          self.history['device'], 
                                          self.history['size']) 
                    if d == "CPU" and s == self.matrix_size]
        accel_times = [t for t, d, s in zip(self.history['time'], 
                                          self.history['device'], 
                                          self.history['size']) 
                    if d in ["GPU", "MPS"] and s == self.matrix_size]
        
        if cpu_times and accel_times:
            speedup = np.mean(cpu_times) / np.mean(accel_times)
            self.history['speedup'].append(speedup)
        else:
            self.history['speedup'].append(None)
        
        self.update_plots()
        
    def update_plots(self):
        """Update visualization"""
        # Clear plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Plot 1: Time series scatter
        self.ax1.set_xlabel('Computation Number', fontsize=12)
        self.ax1.set_ylabel('Time (seconds)', fontsize=12)
        self.ax1.set_title('Computation Time Over Runs', fontsize=13)
        self.ax1.grid(True, alpha=0.3)
        
        cpu_indices = [i for i, d in enumerate(self.history['device']) if d == "CPU"]
        gpu_indices = [i for i, d in enumerate(self.history['device']) if d == "GPU"]
        mps_indices = [i for i, d in enumerate(self.history['device']) if d == "MPS"]
        
        if cpu_indices:
            cpu_times = [self.history['time'][i] for i in cpu_indices]
            self.ax1.scatter(cpu_indices, cpu_times, c='red', s=100, 
                           label='CPU', alpha=0.6, edgecolors='darkred', linewidth=2)
        
        if gpu_indices:
            gpu_times = [self.history['time'][i] for i in gpu_indices]
            self.ax1.scatter(gpu_indices, gpu_times, c='green', s=100, 
                           label='GPU', alpha=0.6, edgecolors='darkgreen', linewidth=2)
        
        if mps_indices:
            mps_times = [self.history['time'][i] for i in mps_indices]
            self.ax1.scatter(mps_indices, mps_times, c='blue', s=100, 
                           label='MPS', alpha=0.6, edgecolors='darkblue', linewidth=2)
        
        # Add trend lines
        if len(cpu_indices) > 1:
            self.ax1.plot(cpu_indices, [self.history['time'][i] for i in cpu_indices], 
                         'r--', alpha=0.3, linewidth=2)
        if len(gpu_indices) > 1:
            self.ax1.plot(gpu_indices, [self.history['time'][i] for i in gpu_indices], 
                         'g--', alpha=0.3, linewidth=2)
        if len(mps_indices) > 1:
            self.ax1.plot(mps_indices, [self.history['time'][i] for i in mps_indices], 
                         'b--', alpha=0.3, linewidth=2)
        
        self.ax1.legend(fontsize=11)
        
        # Auto-adjust y-axis
        if self.history['time']:
            max_time = max(self.history['time'])
            self.ax1.set_ylim(0, max_time * 1.1)
        
        # Plot 2: Performance comparison by matrix size
        self.ax2.set_xlabel('Matrix Size', fontsize=12)
        self.ax2.set_ylabel('Computation Time (seconds)', fontsize=12)
        self.ax2.set_title('CPU vs GPU Performance', fontsize=13)
        self.ax2.grid(True, alpha=0.3)
        
        # Group by size and device
        unique_sizes = sorted(set(self.history['size']))
        cpu_avg_times = []
        gpu_avg_times = []
        mps_avg_times = []
        
        for size in unique_sizes:
            cpu_t = [t for t, d, s in zip(self.history['time'], 
                                         self.history['device'], 
                                         self.history['size']) 
                    if d == "CPU" and s == size]
            gpu_t = [t for t, d, s in zip(self.history['time'], 
                                         self.history['device'], 
                                         self.history['size']) 
                    if d == "GPU" and s == size]
            mps_t = [t for t, d, s in zip(self.history['time'], 
                                         self.history['device'], 
                                         self.history['size']) 
                    if d == "MPS" and s == size]
            
            cpu_avg_times.append(np.mean(cpu_t) if cpu_t else None)
            gpu_avg_times.append(np.mean(gpu_t) if gpu_t else None)
            mps_avg_times.append(np.mean(mps_t) if mps_t else None)
        
        if any(t is not None for t in cpu_avg_times):
            valid_cpu = [(s, t) for s, t in zip(unique_sizes, cpu_avg_times) if t is not None]
            if valid_cpu:
                sizes_cpu, times_cpu = zip(*valid_cpu)
                self.ax2.plot(sizes_cpu, times_cpu, 'ro-', label='CPU', 
                            linewidth=2, markersize=10, alpha=0.7)
        
        if any(t is not None for t in gpu_avg_times):
            valid_gpu = [(s, t) for s, t in zip(unique_sizes, gpu_avg_times) if t is not None]
            if valid_gpu:
                sizes_gpu, times_gpu = zip(*valid_gpu)
                self.ax2.plot(sizes_gpu, times_gpu, 'go-', label='GPU', 
                            linewidth=2, markersize=10, alpha=0.7)
        
        if any(t is not None for t in mps_avg_times):
            valid_mps = [(s, t) for s, t in zip(unique_sizes, mps_avg_times) if t is not None]
            if valid_mps:
                sizes_mps, times_mps = zip(*valid_mps)
                self.ax2.plot(sizes_mps, times_mps, 'bo-', label='MPS', 
                            linewidth=2, markersize=10, alpha=0.7)
        
        self.ax2.legend(fontsize=11)
        
        # Update device info
        accelerator_available = "✓ Available" if self.device.type != "cpu" else "✗ Not Available"
        device_name = ""
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
        elif torch.backends.mps.is_available():
            device_name = "Apple Silicon (MPS)"
        else:
            device_name = "N/A"
        
        speedup_text = ""
        
        if self.history['speedup'] and self.history['speedup'][-1] is not None:
            speedup_text = f"\nSpeedup: {self.history['speedup'][-1]:.2f}x"
        
        self.device_text.set_text(f'Current: {self.current_device}\n'
                                 f'Matrix Size: {self.matrix_size}x{self.matrix_size}\n'
                                 f'Accelerator: {accelerator_available}\n'
                                 f'Device: {device_name}'
                                 f'{speedup_text}')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.97])
        self.fig.canvas.draw()
    
    def on_key(self, event):
        """Handle key presses"""
        if event.key == 'd' or event.key == 'D':
            # Switch device
            if self.current_device == "CPU":
                if torch.cuda.is_available():
                    self.current_device = "GPU"
                    print("Switched to GPU")
                elif torch.backends.mps.is_available():
                    self.current_device = "MPS"
                    print("Switched to MPS (Apple Silicon)")
                else:
                    print("No accelerator available! Staying on CPU")
            else:
                self.current_device = "CPU"
                print("Switched to CPU")
            
            # Run computation on new device
            self.run_computation()
            
        elif event.key == '+' or event.key == '=':
            # Increase workload
            self.matrix_size = min(self.matrix_size + 500, 5000)
            print(f"Increased matrix size to {self.matrix_size}x{self.matrix_size}")
            self.run_computation()
            
        elif event.key == '-' or event.key == '_':
            # Decrease workload
            self.matrix_size = max(self.matrix_size - 500, 500)
            print(f"Decreased matrix size to {self.matrix_size}x{self.matrix_size}")
            self.run_computation()
    
    def run(self):
        """Start the demo"""
        # Connect key press event
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
        # Run initial computation
        print("Starting demo...")
        print("Press [D] to switch between CPU/MPS/GPU")
        print("Press [+] to increase workload")
        print("Press [-] to decrease workload")
        print("\nRunning initial computation...")
        
        self.run_computation()
        
        plt.show()

# Run the demo
if __name__ == "__main__":
    demo = CPUvsGPUDemo()
    demo.run()