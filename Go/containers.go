// First install Go, then execute 'go env'. Select a folder as workspace ~/code/go, set it as GOPATH and append to PATH
// go build containers.go
// go run containers.go

package main
import (
	"io"
	"os"
	"github.com/docker/engine-api/client"
	"github.com/docker/engine-api/types"
	"github.com/docker/engine-api/types/container"
	"golang.org/x/net/context"
)

func main() {
	os.Setenv("DOCKER_HOST", "tcp://192.168.99.103:2376")
	os.Setenv("DOCKER_TLS_VERIFY", "1")
	os.Setenv("DOCKER_CERT_PATH", "/Users/pmacharl/.docker/machine/machines/node1")
	
	ctx := context.Background()
	cli, err := client.NewEnvClient()
	if err != nil {
		panic(err)
	}

	_, err = cli.ImagePull(ctx, "alpine", types.ImagePullOptions{})
	if err != nil {
		panic(err)
	}

	resp, err := cli.ContainerCreate(ctx, &container.Config{
		Image: "alpine",
		Cmd:   []string{"echo", "hello world"},
	}, nil, nil, "")
	if err != nil {
		panic(err)
	}

	if err := cli.ContainerStart(ctx, resp.ID, types.ContainerStartOptions{}); err != nil {
		panic(err)
	}

	if _, err = cli.ContainerWait(ctx, resp.ID); err != nil {
		panic(err)
	}

	out, err := cli.ContainerLogs(ctx, resp.ID, types.ContainerLogsOptions{ShowStdout: true})
	if err != nil {
		panic(err)
	}

	io.Copy(os.Stdout, out)
}