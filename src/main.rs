use std::process;
use std::fs::File;
use std::io::{BufRead, BufReader};
use rand::seq::SliceRandom;
use image::{DynamicImage, GenericImageView};
use aws_config::meta::region::RegionProviderChain;
use aws_sdk_dynamodb::Client;
use aws_sdk_dynamodb::model::AttributeValue;
use lambda_runtime::{handler_fn, Context, Error as LambdaError};
use serde::Deserialize;
use serde_json::{json, Value};
use uuid::Uuid;

#[tokio::main]
async fn main () -> Result < (), LambdaError > {
    let func = handler_fn ( handler ) ;
    lambda_runtime :: run ( func ) . await ? ;
    Ok ( () )
}

#[derive(Debug)]
struct Card {
    name: String,
    img_path: String,
    fortune_telling: Vec<String>,
}

#[derive(Deserialize)]
struct Request {
    name: String,
}

aysnc fn handler ( event: Value , _ctx: Context ) -> Result < Value , LambdaError > {
    let request: Request = serde_json :: from_value ( event ) ? ;
    let mut rng = rand :: thread_rng ( ) ;
    let mut cards = Vec :: new ( ) ;
    let mut fortunes = Vec :: new ( ) ;
    let mut card = Card {
        name: String :: new ( ) ,
        img_path: String :: new ( ) ,
        fortune_telling: Vec :: new ( ) ,
    } ;

    let file = File :: open ( "cards.txt" ) ? ;
    let reader = BufReader :: new ( file ) ;
    for line in reader.lines ( ) {
        let line = line ? ;
        let mut split = line.split ( "," ) ;
        card.name = split . next ( ) . unwrap ( ) . to_string ( ) ;
        card.img_path = split . next ( ) . unwrap ( ) . to_string ( ) ;
        card.fortune_telling = split . map ( | s | s . to_string ( ) ) . collect ( ) ;
        cards . push ( card . clone ( ) ) ;
    }

    let card = cards . choose ( & mut rng ) . unwrap ( ) ;
    let fortune = card . fortune_telling . choose ( & mut rng ) . unwrap ( ) ;

    let region_provider = RegionProviderChain :: default_provider ( ) . or_else ( "ap-northeast-1" ) ? ;
    let client = Client :: new ( & region_provider ) ;
    let mut item = std :: collections :: HashMap :: new ( ) ;
    item . insert ( "id" . to_string ( ) , AttributeValue :: s ( Uuid :: new_v4 ( ) . to_string ( ) ) ) ;
    item . insert ( "name" . to_string ( ) , AttributeValue :: s ( request . name ) ) ;
    item . insert ( "fortune" . to_string ( ) , AttributeValue :: s ( fortune . to_string ( ) ) ) ;
    let input = aws_sdk_dynamodb :: model :: PutItemInput {
        table_name: "fortune-telling".to_string(),
        item,
        ..Default::default()
    };
    let _ = client.put_item(input).await?;

    let img = image::open(card.img_path)?;
    let mut img_buf = Vec::new();
    img.write_to
    let img = image::open(card.img_path)?;
    let mut img_buf = Vec::new();
    img.write_to(&mut img_buf, image::ImageOutputFormat::Png)?;
    let img_base64 = base64::encode(img_buf);

    request.send().await?;

    Ok(json!({
        "fortune": fortune,
        "img": img_base64,
    }))

}



