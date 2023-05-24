package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/jedib0t/go-pretty/v6/table"
)

type Target struct {
	conn        net.Conn
	address     string
	connectTime string
}

var (
	targets   []Target
	killFlag  int
	sock      net.Listener
	waitGroup sync.WaitGroup
)

func listenerHandler(hostIP string, hostPort int) {
	defer waitGroup.Done()

	address := fmt.Sprintf("%s:%d", hostIP, hostPort)
	var err error
	sock, err = net.Listen("tcp", address)
	if err != nil {
		fmt.Printf("[-] Failed to bind to %s\n", address)
		return
	}

	fmt.Println("[+] Awaiting connection from client...")
	for {
		conn, err := sock.Accept()
		if killFlag == 1 {
			break
		}
		if err != nil {
			fmt.Println("[-] Error accepting connection:", err)
			continue
		}

		go communicationHandler(conn)
	}
}

func targetCommChannel(target Target) {
	for {
		fmt.Print("send message#> ")
		var message string
		fmt.Scan(&message)

		communicationOut(target.conn, message)
		if message == "exit" {
			target.conn.Close()
			break
		}
		if message == "background" {
			break
		} else {
			response := communicationIn(target.conn)
			if response == "exit" {
				fmt.Println("[-] The client has terminated the session.")
				target.conn.Close()
				break
			}
			fmt.Println(response)
		}
	}
}

func communicationHandler(conn net.Conn) {
	remoteAddr := conn.RemoteAddr().String()

	currentTime := time.Now().Format("01/02/2006 15:04:05")
	target := Target{conn: conn, address: remoteAddr, connectTime: currentTime}
	targets = append(targets, target)

	fmt.Printf("\n[+] Connection received from %s\nEnter command#> ", remoteAddr)
}

func communicationIn(conn net.Conn) string {
	fmt.Println("[+] Awaiting response...")
	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	if err != nil {
		fmt.Println("[-] Error reading response:", err)
		return ""
	}
	return string(buf[:n])
}

func communicationOut(conn net.Conn, message string) {
	_, err := conn.Write([]byte(message))
	if err != nil {
		fmt.Println("[-] Error sending message:", err)
	}
}

func main() {
	fmt.Println("Your banner here")

	targets = []Target{}
	killFlag = 0

	if len(os.Args) < 3 {
		fmt.Println("[-] Command line argument(s) missing.  Please try again.")
		return
	}

	hostIP := os.Args[1]
	hostPort, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Println("[-] Invalid port number.")
		return
	}

	waitGroup.Add(1)
	go listenerHandler(hostIP, hostPort)

	for {
		fmt.Print("Enter command#> ")
		var command string
		fmt.Scan(&command)

		if command == "exit" {
			killFlag = 1
			sock.Close()
			break
		}

		parts := strings.Split(command, " ")
		if parts[0] == "sessions" {
			if len(parts) < 2 {
				continue
			}

			if parts[1] == "-l" {
				t := table.NewWriter
				t.AppendHeader(table.Row{"Session", "Target"})
				for i, target := range targets {
					t.AppendRow([]interface{}{i, target.address})
				}
				fmt.Println(t.Render())
			} else if parts[1] == "-i" {
				if len(parts) < 3 {
					continue
				}

				num, err := strconv.Atoi(parts[2])
				if err != nil || num >= len(targets) || num < 0 {
					fmt.Println("[-] Invalid session number.")
					continue
				}

				target := targets[num]
				targetCommChannel(target)
			}
		}
	}
	waitGroup.Wait()
}
