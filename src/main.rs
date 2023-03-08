use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use rand::seq::SliceRandom;
use image::{DynamicImage, GenericImageView};

#[derive(Debug)]
struct Card {
    name: String,
    img_path: String,
    fortune_telling: Vec<String>,
}

impl Clone for Card {
    fn clone(&self) -> Self {
        Card {
            name: self.name.clone(),
            img_path: self.img_path.clone(),
            fortune_telling: self.fortune_telling.clone(),
        }
    }
}

impl Card {
    fn new(name: String, img_path: String, fortune_telling: Vec<String>) -> Card {
        Card { name, img_path, fortune_telling }
    }
    fn from_csv_line(line: &str) -> Option<Card> {
        let values: Vec<&str> = line.trim().split(",").collect();
        if values.len() == 4 {
            Some(Card::new(
                String::from(values[0]),
                String::from(values[1]),
                vec![
                    String::from(values[2]),
                    String::from(values[3]),
                ],
            ))
        } else {
            None
        }
    }
    // showing the image from archive cards

    fn show_image(&self) -> Option<DynamicImage> {
        match image::open(&self.img_path) {
            Ok(img) => Some(img),
            Err(e) => {
                eprintln!("Error: {}", e);
                None
            }
        }
    }
}

fn read_cards_from_csv(csv_path: &str) -> Vec<Card> {
    let file = match File::open(csv_path) {
        Ok(file) => file,
        Err(e) => {
            eprintln!("Error: {}", e);
            process::exit(1);
        }
    };

    let reader = BufReader::new(file);
    reader
        .lines()
        .filter_map(|line| Card::from_csv_line(&line.unwrap()))
        .collect()
}

fn main() {
    let cards = read_cards_from_csv("tarot.csv");

    let mut rng = rand::thread_rng();
    let chosen_cards = cards
        .choose_multiple(&mut rng, 3)
        .cloned()
        .collect::<Vec<Card>>();

    for card in &chosen_cards {
        println!("

{}", card.name);

        if let Some(img) = card.show_image() {
            let (width, height) = img.dimensions();
            let resized_img = img.resize(width / 2, height / 2, image::imageops::FilterType::Nearest);
            resized_img.save("card.png").unwrap();
            println!("

{}", card.fortune_telling[0]);
            println!("

{}", card.fortune_telling[1]);
        }
    }
}

// create a web app
use actix_web::{web, App, HttpResponse, HttpServer, Responder};

async fn index() -> impl Responder {
    HttpResponse::Ok().body("Hello world!")
}

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().route("/", web::get().to(index)))
        .bind("
        