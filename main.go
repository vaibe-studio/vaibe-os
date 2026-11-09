package main

import (
	"embed"
	"fmt"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

//go:embed all:skeleton skeleton/.gitattributes skeleton/.gitignore skeleton/.env.example
var skeletonFS embed.FS

const version = "v0.1.0-alpha"

const usage = `vaibe-os — the operating layer for your AI agents

Usage:
  vaibe-os init <folder> [--name <name>]   create a new instance workspace
  vaibe-os version                          print version
  vaibe-os validate                         (planned: validate instance structure)
  vaibe-os doctor                           (planned: runtime invariants)
  vaibe-os connect <instance>               (planned: link to another instance)
`

func main() {
	if len(os.Args) < 2 {
		fmt.Fprint(os.Stderr, usage)
		os.Exit(1)
	}
	switch os.Args[1] {
	case "init":
		if err := runInit(os.Args[2:]); err != nil {
			fmt.Fprintf(os.Stderr, "vaibe-os init: %v\n", err)
			os.Exit(1)
		}
	case "version":
		fmt.Println("vaibe-os", version)
	case "validate", "doctor", "connect":
		fmt.Printf("vaibe-os %s: not implemented yet (planned for v0.1.x)\n", os.Args[1])
	default:
		fmt.Fprintf(os.Stderr, "unknown command: %s\n\n%s", os.Args[1], usage)
		os.Exit(1)
	}
}

func runInit(args []string) error {
	var folder, name string
	for i := 0; i < len(args); i++ {
		switch args[i] {
		case "--name":
			if i+1 >= len(args) {
				return fmt.Errorf("--name requires a value")
			}
			i++
			name = args[i]
		default:
			if folder != "" {
				return fmt.Errorf("unexpected argument: %s", args[i])
			}
			folder = args[i]
		}
	}
	if folder == "" {
		return fmt.Errorf("usage: vaibe-os init <folder> [--name <name>]")
	}
	if name == "" {
		name = filepath.Base(folder)
	}

	if _, err := os.Stat(folder); err == nil {
		entries, _ := os.ReadDir(folder)
		if len(entries) > 0 {
			return fmt.Errorf("target %s already exists and is not empty", folder)
		}
	}

	if err := os.MkdirAll(folder, 0o755); err != nil {
		return err
	}
	if err := fs.WalkDir(skeletonFS, "skeleton", func(p string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		rel, _ := filepath.Rel("skeleton", p)
		if rel == "." {
			return nil
		}
		dst := filepath.Join(folder, rel)
		if d.IsDir() {
			return os.MkdirAll(dst, 0o755)
		}
		data, err := skeletonFS.ReadFile(p)
		if err != nil {
			return err
		}
		out := strings.ReplaceAll(string(data), "{{INSTANCE_NAME}}", name)
		return os.WriteFile(dst, []byte(out), 0o644)
	}); err != nil {
		return fmt.Errorf("copy skeleton: %w", err)
	}

	if err := gitInit(folder); err != nil {
		fmt.Fprintf(os.Stderr, "warning: git init skipped (%v)\n", err)
	}

	fmt.Printf("Instance created: %s (%s)\n", folder, name)
	fmt.Println("Next: open the folder in your AI harness and start working.")
	return nil
}

func gitInit(dir string) error {
	cmd := exec.Command("git", "init", "-b", "main")
	cmd.Dir = dir
	return cmd.Run()
}
