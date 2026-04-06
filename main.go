package main

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"os"
	"runtime"
	"sync"
	"sync/atomic"
	"syscall"
	"time"

	"fyne.io/fyne/v2"
	fyneapp "fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
	"golang.design/x/hotkey"
)

// ==================== CONSTANTS ====================

const (
	KeySpace = 0x20
	Key1     = 0x31
	Key2     = 0x32
)

// Timing configuration (in milliseconds)
const (
	MinPressDuration  = 20 // ms
	MaxPressDuration  = 40 // ms
	MinClickInterval  = 10 // ms
	MaxClickInterval  = 40 // ms
	InactiveLoopDelay = 50 // ms
)

// ==================== WINDOWS API ====================

var (
	user32         = syscall.NewLazyDLL("user32.dll")
	procKeybdEvent = user32.NewProc("keybd_event")
)

// keyDown simulates pressing a key down
func keyDown(key byte) error {
	ret, _, err := procKeybdEvent.Call(uintptr(key), 0, 0, 0)
	if ret == 0 {
		return fmt.Errorf("keybd_event(DOWN) failed for key 0x%X: %w", key, err)
	}
	return nil
}

// keyUp simulates releasing a key
func keyUp(key byte) error {
	ret, _, err := procKeybdEvent.Call(uintptr(key), 0, 2, 0)
	if ret == 0 {
		return fmt.Errorf("keybd_event(UP) failed for key 0x%X: %w", key, err)
	}
	return nil
}

// ==================== CLICKER APP STRUCT ====================

// ClickerApp encapsulates the auto-clicker application state
type ClickerApp struct {
	// State management
	running int32 // atomic bool (0 = false, 1 = true)
	clicks  int64 // atomic counter

	// Timing
	totalActiveTime time.Duration
	lastStartTime   time.Time
	mu              sync.RWMutex // protects timing fields

	// UI Components
	countLabel  *widget.Label
	statusLabel *widget.Label
	timeLabel   *widget.Label
	toggleBtn   *widget.Button
	mainWindow  fyne.Window

	// Context for graceful shutdown
	ctx    context.Context
	cancel context.CancelFunc
}

// ==================== PUBLIC METHODS ====================

// IsRunning returns true if the clicker is currently active
func (app *ClickerApp) IsRunning() bool {
	return atomic.LoadInt32(&app.running) == 1
}

// SetRunning sets the running state
func (app *ClickerApp) SetRunning(state bool) {
	var val int32 = 0
	if state {
		val = 1
	}
	atomic.StoreInt32(&app.running, val)
}

// GetClickCount returns the current click counter
func (app *ClickerApp) GetClickCount() int64 {
	return atomic.LoadInt64(&app.clicks)
}

// IncrementClicks increments the click counter by delta
func (app *ClickerApp) IncrementClicks(delta int64) {
	atomic.AddInt64(&app.clicks, delta)
}

// ToggleRunning toggles the running state
func (app *ClickerApp) ToggleRunning() {
	app.mu.Lock()
	defer app.mu.Unlock()

	wasRunning := app.IsRunning()
	newState := !wasRunning

	if newState {
		// Starting
		app.lastStartTime = time.Now()
		app.SetRunning(true)
		app.updateStatusUI("Статус: ✓ ВКЛ", "Выключить (Tab)")
	} else {
		// Stopping - accumulate active time
		app.totalActiveTime += time.Since(app.lastStartTime)
		app.SetRunning(false)
		app.updateStatusUI("Статус: ○ ВЫКЛ", "Включить (Tab)")
	}
}

// GetActiveTime returns the total accumulated active time
func (app *ClickerApp) GetActiveTime() time.Duration {
	app.mu.RLock()
	defer app.mu.RUnlock()

	totalTime := app.totalActiveTime
	if app.IsRunning() {
		totalTime += time.Since(app.lastStartTime)
	}
	return totalTime
}

// ShowStats displays statistics to stdout
func (app *ClickerApp) ShowStats() {
	clicks := app.GetClickCount()
	activeTime := app.GetActiveTime()
	fmt.Printf("\n\n=== СТАТИСТИКА ===\n")
	fmt.Printf("Накликано: %d\n", clicks)
	fmt.Printf("Общее время в работе: %s\n\n", activeTime.Round(time.Second))
}

// ==================== PRIVATE UI METHODS ====================

// updateStatusUI safely updates status labels from any goroutine
func (app *ClickerApp) updateStatusUI(statusText, buttonText string) {
	fyne.Do(func() {
		if app.statusLabel != nil {
			app.statusLabel.SetText(statusText)
		}
		if app.toggleBtn != nil {
			app.toggleBtn.SetText(buttonText)
		}
	})
}

// updateCountUI safely updates click count display
func (app *ClickerApp) updateCountUI() {
	count := app.GetClickCount()
	text := fmt.Sprintf("Накликано: %d", count)

	fyne.Do(func() {
		if app.countLabel != nil {
			app.countLabel.SetText(text)
		}
	})
}

// updateTimeUI safely updates time display
func (app *ClickerApp) updateTimeUI(totalTime time.Duration) {
	hours := int(totalTime.Hours())
	minutes := int(totalTime.Minutes()) % 60
	seconds := int(totalTime.Seconds()) % 60

	text := fmt.Sprintf("Время в работе: %02d:%02d:%02d", hours, minutes, seconds)
	fyne.Do(func() {
		if app.timeLabel != nil {
			app.timeLabel.SetText(text)
		}
	})
}

// ==================== WORKER GOROUTINES ====================

// pressKeys simulates pressing space + 1 + 2 simultaneously
func (app *ClickerApp) pressKeys() error {
	if err := keyDown(KeySpace); err != nil {
		return fmt.Errorf("keyDown(Space): %w", err)
	}
	if err := keyDown(Key1); err != nil {
		_ = keyUp(KeySpace) // attempt cleanup
		return fmt.Errorf("keyDown(1): %w", err)
	}
	if err := keyDown(Key2); err != nil {
		_ = keyUp(KeySpace) // attempt cleanup
		_ = keyUp(Key1)
		return fmt.Errorf("keyDown(2): %w", err)
	}

	// Press duration with jitter
	pressDuration := time.Duration(MinPressDuration+rand.Intn(MaxPressDuration-MinPressDuration)) * time.Millisecond
	time.Sleep(pressDuration)

	// Release all keys
	if err := keyUp(KeySpace); err != nil {
		log.Printf("Warning: keyUp(Space) failed: %v", err)
	}
	if err := keyUp(Key1); err != nil {
		log.Printf("Warning: keyUp(1) failed: %v", err)
	}
	if err := keyUp(Key2); err != nil {
		log.Printf("Warning: keyUp(2) failed: %v", err)
	}

	return nil
}

// startClickerLoop is the main clicking worker
func (app *ClickerApp) startClickerLoop() {
	ticker := time.NewTicker(1 * time.Millisecond) // high-resolution ticker
	defer ticker.Stop()

	for {
		select {
		case <-app.ctx.Done():
			log.Println("Clicker loop shutting down")
			return
		case <-ticker.C:
			if app.IsRunning() {
				if err := app.pressKeys(); err != nil {
					log.Printf("Error pressing keys: %v", err)
					continue
				}

				app.IncrementClicks(2) // Space + 1 + 2 = 2 actions
				app.updateCountUI()

				// Click interval with jitter
				interval := time.Duration(MinClickInterval+rand.Intn(MaxClickInterval-MinClickInterval)) * time.Millisecond
				time.Sleep(interval)
			} else {
				// Not running, use lighter sleep to reduce CPU usage
				time.Sleep(time.Duration(InactiveLoopDelay) * time.Millisecond)
			}
		}
	}
}

// startTimerLoop updates the display timer every second
func (app *ClickerApp) startTimerLoop() {
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-app.ctx.Done():
			log.Println("Timer loop shutting down")
			return
		case <-ticker.C:
			activeTime := app.GetActiveTime()
			app.updateTimeUI(activeTime)
		}
	}
}

// startHotkeyListener registers the Tab hotkey
func (app *ClickerApp) startHotkeyListener(parentWindow fyne.Window) {
	hkTab := hotkey.New([]hotkey.Modifier{}, hotkey.KeyTab)
	if err := hkTab.Register(); err != nil {
		log.Printf("ERROR: Failed to register Tab hotkey: %v", err)
		dialog.ShowError(
			fmt.Errorf("не удалось зарегистрировать горячую клавишу Tab: %v", err),
			parentWindow,
		)
		return
	}

	log.Println("Tab hotkey registered successfully")

	go func() {
		for {
			select {
			case <-app.ctx.Done():
				if err := hkTab.Unregister(); err != nil {
					log.Printf("Warning: Failed to unregister hotkey: %v", err)
				}
				return
			case <-hkTab.Keydown():
				app.ToggleRunning()
			}
		}
	}()
}

// ==================== APP INITIALIZATION ====================

// NewClickerApp creates a new instance of ClickerApp
func NewClickerApp() *ClickerApp {
	ctx, cancel := context.WithCancel(context.Background())
	return &ClickerApp{
		running:         0,
		clicks:          0,
		totalActiveTime: 0,
		ctx:             ctx,
		cancel:          cancel,
	}
}

// BuildUI constructs the user interface
func (app *ClickerApp) BuildUI() fyne.CanvasObject {
	app.countLabel = widget.NewLabelWithStyle(
		"Накликано: 0",
		fyne.TextAlignCenter,
		fyne.TextStyle{Bold: true},
	)
	app.countLabel.Importance = widget.HighImportance

	app.statusLabel = widget.NewLabel("Статус: ○ ВЫКЛ")
	app.statusLabel.TextStyle = fyne.TextStyle{Bold: true}

	app.timeLabel = widget.NewLabel("Время в работе: 00:00:00")
	app.timeLabel.TextStyle = fyne.TextStyle{Bold: true}

	app.toggleBtn = widget.NewButton("Включить (Tab)", func() {
		app.ToggleRunning()
	})

	exitButton := widget.NewButton("Выход", func() {
		app.ShowStats()
		app.cancel()                       // signal all goroutines to stop
		time.Sleep(100 * time.Millisecond) // allow goroutines to exit
		app.mainWindow.Close()
	})

	content := container.NewVBox(
		widget.NewLabel("Автокликер • Space + 1 + 2"),
		app.countLabel,
		app.statusLabel,
		app.timeLabel,
		widget.NewSeparator(),
		app.toggleBtn,
		exitButton,
	)

	return content
}

// ==================== MAIN FUNCTION ====================

func main() {
	// Validate OS
	if runtime.GOOS != "windows" {
		fmt.Println("This application only works on Windows")
		os.Exit(1)
	}

	// Setup logging
	log.SetFlags(log.LstdFlags | log.Lshortfile)
	log.Println("Starting Bongo Cat Auto-Clicker")

	// Create app instance
	app := NewClickerApp()

	// Create Fyne app and window
	fyneApp := fyneapp.New()
	fyneApp.Settings().SetTheme(theme.DarkTheme())
	w := fyneApp.NewWindow("Bongo Cat Автокликер")
	w.Resize(fyne.NewSize(205, 250))
	w.CenterOnScreen()
	app.mainWindow = w

	// Build and show UI
	w.SetContent(app.BuildUI())
	w.Show()

	// Start worker goroutines
	go app.startClickerLoop()
	go app.startTimerLoop()
	app.startHotkeyListener(w)

	// Handle window close
	w.SetOnClosed(func() {
		log.Println("Window closed, shutting down...")
		app.ShowStats()
		app.cancel()
	})

	log.Println("Initialization complete. Starting Fyne event loop")

	// Run Fyne event loop (blocks until window closes)
	fyneApp.Run()

	log.Println("Application terminated")
}
