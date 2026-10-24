pub fn format_duration(seconds: f64) -> String {
    let total = seconds as u64;
    let (hours, minutes, secs) = (total / 3600, total / 60 % 60, total % 60);
    match total {
        0..60 => format!("{total} s"),
        60..3600 => format!("{minutes}:{secs:02}"),
        _ => format!("{hours}:{minutes:02}:{secs:02}"),
    }
}

pub fn clicks_text(count: u64) -> String {
    let digits = count.to_string();
    let mut grouped = String::new();
    for (i, c) in digits.chars().enumerate() {
        if i > 0 && (digits.len() - i) % 3 == 0 {
            grouped.push(',');
        }
        grouped.push(c);
    }
    format!("{grouped} {}", if count == 1 { "click" } else { "clicks" })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn durations() {
        assert_eq!(format_duration(59.9), "59 s");
        assert_eq!(format_duration(61.0), "1:01");
        assert_eq!(format_duration(3725.0), "1:02:05");
    }

    #[test]
    fn click_counts() {
        assert_eq!(clicks_text(1), "1 click");
        assert_eq!(clicks_text(999), "999 clicks");
        assert_eq!(clicks_text(1234567), "1,234,567 clicks");
    }
}
