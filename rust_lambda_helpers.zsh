LAMBDA_ARCH = "linux/arm64"
RUST_TARGET = "aarch64-unknown-linux-gnu" 
RUST_VERSION = "latest"
PROJECT_NAME = "tarot"

al2build() {
	docker run --platform ${LAMBDA_ARCH} \
	  --rm --user "$(id -u)":"$(id -g)" \
	  -v "${PWD}":/usr/src/myapp -w /usr/src/myapp rust:${RUST_VERSION} \
  	cargo build --release --target ${RUST_TARGET} # This line can be any cargo command
}

zipRustLambda() {
	cp ./target/${RUST_TARGET}/release/rust_on_aws ./bootstrap && zip lambda.zip bootstrap && rm bootstrap
}

