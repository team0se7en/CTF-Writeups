package main

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/caarlos0/env"
	"github.com/joho/godotenv"

	uuid "github.com/satori/go.uuid"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Config struct {
	MongoDBHostPort   string `env:"ADDR"`
	MongoDBPassword   string `env:"PASSWORD"`
	MongoDBDbName     string `env:"DB_NAME"`
	MongoDBCollection string `env:"COLLECTION"`
}

var collection *mongo.Collection

type User struct {
	Username string `bson:"username"`
	Password string `bson:"password"`
	Otp      string `bson:"otp"`
}

func exit(message string) {
	fmt.Printf(message)
	os.Exit(0)
}

func actionRegister(username, password string) {
	// find user with the same username
	var result User
	filter := bson.M{"username": username}
	ctx, _ := context.WithTimeout(context.Background(), 5*time.Second)
	err := collection.FindOne(ctx, filter).Decode(&result)
	if err == nil {
		exit("ERROR: user exists")
	}
	otp := fmt.Sprintf("%s", uuid.NewV4())
	ctx, _ = context.WithTimeout(context.Background(), 5*time.Second)
	_, err = collection.InsertOne(ctx, User{username, password, otp})

	if err != nil {
		exit(fmt.Sprintf("ERROR: %s", err))
	} else {
		exit(fmt.Sprintf("SUCCESS: %s", otp))
	}
}

func actionLogin(username, password string) {
	// find user with the same username and password
	var result User
	filter := bson.M{"username": username, "password": password}
	ctx, _ := context.WithTimeout(context.Background(), 5*time.Second)
	err := collection.FindOne(ctx, filter).Decode(&result)
	if err != nil {
		exit("ERROR: user not found")
	}
	otp := fmt.Sprintf("%s", uuid.NewV4())
	ctx, _ = context.WithTimeout(context.Background(), 5*time.Second)
	_, err = collection.UpdateOne(
		ctx,
		bson.M{"username": username, "password": password},
		bson.D{
			{"$set", bson.D{{"otp", otp}}},
		},
	)

	if err != nil {
		exit(fmt.Sprintf("ERROR: %s", err))
	} else {
		exit(fmt.Sprintf("SUCCESS: %s", otp))
	}
}

func main() {
	if err := godotenv.Load(); err != nil {
		log.Printf("File .env not found, reading configuration from ENV")
	}

	// load config from .env
	var cfg Config
	if err := env.Parse(&cfg); err != nil {
		log.Fatalf("Failed to parse ENV")
	}

	// read login and password from stdin
	reader := bufio.NewReader(os.Stdin)
	action, _ := reader.ReadString('\n')
	username, _ := reader.ReadString('\n')
	password, _ := reader.ReadString('\n')

	action = strings.TrimSuffix(action, "\n")
	username = strings.TrimSuffix(username, "\n")
	password = strings.TrimSuffix(password, "\n")

	if action != "register" && action != "login" {
		exit("Error: invalid action")
	}

	// connect to the password protected DB
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(ctx, options.Client().ApplyURI(fmt.Sprintf("mongodb://admin:admin@localhost:27017")))

*
	if err != nil {
		exit("Connection error")
	}
	collection = client.Database("cybrics").Collection("users")

	if action == "register" {
		actionRegister(username, password)
	}
	if action == "login" {
		actionLogin(username, password)
	}
}

