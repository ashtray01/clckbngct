package main

import (
	"fmt"
	"math/rand"
	"os"
	"runtime"
	"sync"
	"syscall"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	"golang.design/x/hotkey"
)

const (
	KEY_SPACE = 0x20
	KEY_1     = 0x31
	KEY_2     = 0x32
)

var (
	user32          = syscall.NewLazyDLL("user32.dll")
	procKeybdEvent  = user32.NewProc("keybd_event")
	running         = false
	contador        int64
	mu              sync.Mutex
	programStart    = time.Now()  // время запуска программы
	totalActiveTime time.Duration // общее накопленное время работы
	activeStart     time.Time     // когда последний раз включили
	countLabel      *widget.Label
	statusLabel     *widget.Label
	timeLabel       *widget.Label
	toggleButton    *widget.Button
)

func keyDown(key byte) {
	procKeybdEvent.Call(uintptr(key), 0, 0, 0)
}

func keyUp(key byte) {
	procKeybdEvent.Call(uintptr(key), 0, 2, 0)
}

func pressKeys() {
	keyDown(KEY_SPACE)
	keyDown(KEY_1)
	keyDown(KEY_2)
	time.Sleep(time.Duration(20+rand.Intn(21)) * time.Millisecond)
	keyUp(KEY_SPACE)
	keyUp(KEY_1)
	keyUp(KEY_2)
}

func updateCount() {
	mu.Lock()
	text := fmt.Sprintf("Накликано: %d", contador)
	mu.Unlock()
	countLabel.SetText(text)
}

func updateTimer() {
	for {
		time.Sleep(1 * time.Second)

		if running {
			// Добавляем прошедшее время с момента последнего включения
			totalActiveTime += time.Since(activeStart)
			activeStart = time.Now() // обновляем точку отсчёта
		}

		// Отображаем общее накопленное время
		h := int(totalActiveTime.Hours())
		m := int(totalActiveTime.Minutes()) % 60
		s := int(totalActiveTime.Seconds()) % 60
		timeLabel.SetText(fmt.Sprintf("Время в работе: %02d:%02d:%02d", h, m, s))
	}
}

func showStats() {
	fmt.Printf("\n\n=== СТАТИСТИКА ===\n")
	fmt.Printf("Накликано: %d\n", contador)
	fmt.Printf("Общее время в работе: %s\n\n", totalActiveTime.Round(time.Second))
}

func toggleRunning() {
	running = !running

	if running {
		activeStart = time.Now()
		statusLabel.SetText("Статус: ✓ ВКЛ")
		toggleButton.SetText("Выключить (Tab)")
	} else {
		// При выключении добавляем оставшееся время
		totalActiveTime += time.Since(activeStart)
		statusLabel.SetText("Статус: ○ ВЫКЛ")
		toggleButton.SetText("Включить (Tab)")
	}
}

func main() {
	if runtime.GOOS != "windows" {
		fmt.Println("Этот скрипт работает только на Windows")
		os.Exit(1)
	}

	rand.Seed(time.Now().UnixNano())

	a := app.New()
	w := a.NewWindow("Bongo Cat Автокликер")
	w.Resize(fyne.NewSize(300, 260))
	w.CenterOnScreen()

	countLabel = widget.NewLabelWithStyle("Накликано: 0", fyne.TextAlignCenter, fyne.TextStyle{Bold: true})
	countLabel.Importance = widget.HighImportance

	statusLabel = widget.NewLabel("Статус: ○ ВЫКЛ")
	statusLabel.TextStyle = fyne.TextStyle{Bold: true}

	timeLabel = widget.NewLabel("Время в работе: 00:00:00")
	timeLabel.TextStyle = fyne.TextStyle{Bold: true}

	toggleButton = widget.NewButton("Включить (Tab)", toggleRunning)

	exitButton := widget.NewButton("Выход", func() {
		showStats()
		a.Quit()
	})

	content := container.NewVBox(
		widget.NewLabel("Автокликер • Space + 1 + 2"),
		countLabel,
		statusLabel,
		timeLabel,
		widget.NewSeparator(),
		toggleButton,
		exitButton,
	)

	w.SetContent(content)
	w.Show()

	// Tab — вкл/выкл
	hkTab := hotkey.New([]hotkey.Modifier{}, hotkey.KeyTab)
	if err := hkTab.Register(); err == nil {
		go func() {
			for range hkTab.Keydown() {
				toggleRunning()
			}
		}()
	}

	// Запуск обновления таймера каждую секунду
	go updateTimer()

	// Основной цикл автокликера
	go func() {
		for {
			if running {
				pressKeys()
				mu.Lock()
				contador++
				mu.Unlock()
				updateCount()
				time.Sleep(time.Duration(10+rand.Intn(31)) * time.Millisecond)
			} else {
				time.Sleep(50 * time.Millisecond)
			}
		}
	}()

	a.Run()
}
