use regex::Regex;
use std::fs::{write, File};
use std::io::prelude::*;
use std::io::BufReader;

fn read_csv(src: &str) -> std::io::Result<String> {
    // Read csv file, return result or error
    let csv_file = File::open(src)?;

    // Create buffer and string to hold the csv data
    let mut buf_reader = BufReader::new(csv_file);
    let mut csv_log = String::new();

    // Read buffer data into the string, return ok(String) or error
    buf_reader.read_to_string(&mut csv_log)?;
    Ok(csv_log)
}

fn correct_timestamps(csv_log: String, output_path: &str) {
    // Create regex to parse time offset, call
    // .unwrap() instead of error checking, regex is valid for these csv logs
    let re = Regex::new(r"\+[0-9]{2}-[0-9]{2}").unwrap();

    // Run the regex over the csv_log, replace with empty string
    let correct_csv_log = re.replace_all(&csv_log, "").to_string();

    // Write correct log to output_path with optional error message
    write(output_path, &correct_csv_log).expect("Unable to write csv_log");
}

fn main() {
    // Base path indicating alignment root folder (3 directories up)
    let alignment_path = "../../../Data/Alignments/";

    // Array of alignments, no need to unzip .gz
    let alignments_fnames = [
        "2-way.csv.gz",
        "3-way-invoice-after-GR.csv.gz",
        "3-way-invoice-before-GR-split1.csv.gz",
        "3-way-invoice-before-GR-split2.csv.gz",
        "3-way-invoice-before-GR-split3.csv.gz",
        "3-way-invoice-before-GR-split4.csv.gz",
        "3-way-invoice-before-GR-split5.csv.gz",
        "3-way-invoice-before-GR-split5.csv.gz",
    ];

    // Loop through iterator from alignment_fnames
    for fname in alignments_fnames.iter() {
        // Specificy input (path) and parse the csv log
        let path = format!("{}/{}", alignment_path, fname.to_string());
        let csv_log = read_csv(&path).unwrap();

        // Run the regex and write the corrected csv log
        correct_timestamps(csv_log, &path);
    }
}
