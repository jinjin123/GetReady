package main

import (
	"github.com/gin-gonic/gin"
	"gopkg.in/olahol/melody.v1"
	//"net/http"
)

type FOO struct{
	//TIME string  `json:"time" binding:"required"`
	DATA []string `json:"data" binding:"required"`
}

func main() {
	r := gin.Default()
	m := melody.New()

	//r.POST("/echo", func(c *gin.Context) {
	//	m.HandleRequest(c.Writer,c.Request)
		//http.ServeFile(c.Writer, c.Request, "index.html")
	//})
	//r.POST("/data", func(c *gin.Context){
	//		//var time FOO
	//		var data FOO
	//		//c.BindJSON(&time)
	//		c.BindJSON(&data)
	//		m.HandleRequest(c.Writer,c.Request)
	//		fmt.Printf("URL to store: %s\n",data)
	//})
	r.GET("/", func(c *gin.Context) {
		m.HandleRequest(c.Writer, c.Request)
	})


	m.HandleMessage(func(s *melody.Session, msg []byte) {
		//fmt.Println(string(msg[:]))
		m.Broadcast(msg)
	})

	r.Run(":5000")
}

