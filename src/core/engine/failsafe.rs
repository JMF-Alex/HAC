use crate::core::storage::config::Failsafe;

const CORNER_MARGIN: i32 = 2;

pub fn corner_hit(corner: Failsafe, x: i32, y: i32, width: i32, height: i32) -> bool {
    let near = |v: i32, edge: i32| (edge - CORNER_MARGIN..=edge + CORNER_MARGIN).contains(&v);
    let (left, right, top, bottom) = (near(x, 0), near(x, width - 1), near(y, 0), near(y, height - 1));
    match corner {
        Failsafe::Off => false,
        Failsafe::TopLeft => left && top,
        Failsafe::TopRight => right && top,
        Failsafe::BottomLeft => left && bottom,
        Failsafe::BottomRight => right && bottom,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn corners() {
        let (w, h) = (1920, 1080);
        assert!(corner_hit(Failsafe::TopLeft, 0, 1, w, h));
        assert!(corner_hit(Failsafe::TopRight, 1919, 0, w, h));
        assert!(corner_hit(Failsafe::BottomLeft, 2, 1077, w, h));
        assert!(corner_hit(Failsafe::BottomRight, 1921, 1079, w, h));
        assert!(!corner_hit(Failsafe::TopLeft, 3, 0, w, h));
        assert!(!corner_hit(Failsafe::TopRight, 0, 0, w, h));
        assert!(!corner_hit(Failsafe::Off, 0, 0, w, h));
    }
}
