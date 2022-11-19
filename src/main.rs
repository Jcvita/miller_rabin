use rand::Rng;
use num_bigint::{BigInt, ToBigInt};

fn calc_s_d(n: i32) -> (i32, i32) {
    //calculate s, d such that n - 1 = (2^s)*d and d must be odd
    let num = n as f32;
    let mut s: i32 = 0;
    let mut d: f32 = num - 1.0;
    while (d/2.0).fract() == 0.0 {
        s += 1;
        d /= 2f32;
    }
    (s, d as i32)
}

// fn miller_rabin(n: BigInt, k: BigInt) -> String {
//     if n % 2 == 0 || n < 3 { return String::from("composite") }

//     let mut rng = rand::thread_rng();
    
//     let (_, d) = calc_s_d(n);
    
//     let a: BigInt = rng.gen_range(2..n-2).to_bigint().unwrap();
//     let mut b = (BigInt::pow(&a, d as u32)) % n; 
//     for _ in 1..k {
//         if b == BigInt::from(1) || b == BigInt::from(-1) { return String::from("probably prime") }
//         b = BigInt::pow(&b, 2);
//         println!("{}", &b);
//         if b == BigInt::from(1) { return String::from("composite") }
//         else if b == BigInt::from(-1) { return String::from("probably prime") }
//     }
//     String::from("probably prime")
// }

fn miller_rabin(n: i32, k: i32) -> String {
    if n % 2 == 0 || n < 3 { return String::from("composite") }
    
    let mut rng = rand::thread_rng();
    let (s, d) = calc_s_d(n);
    // if (n-1) != ((2^s)*d) { panic!("s and d values invalid"); }
    for _ in 1..k {
        let a = rng.gen_range(1..n-1); // generate a random number between 2 and n - 2
        let mut x: BigInt = BigInt::from(a).modpow(&d.to_bigint().unwrap(), &n.to_bigint().unwrap());
        let mut y: BigInt = BigInt::from(0);  // nontrivial square root of 1 modulo n
        for _ in 1..s {
            y = x.modpow(&2.to_bigint().unwrap(), &n.to_bigint().unwrap());
            if y == BigInt::from(1) && x != BigInt::from(1) && x != (n.to_bigint().unwrap() - BigInt::from(1)) {
                return String::from("composite")
            }
            x = y.clone();
        }
        if y != BigInt::from(1) {
            return String::from("composite")
        }
    };
    String::from("probably prime")
}

#[warn(non_snake_case)]
fn main() {
    let n = 53;
    let k = 10;
    let (a, b) = calc_s_d(n);
    println!("s: {} d: {}", a, b);
    let prim = miller_rabin(n, k);
    println!("{}", prim);
    // for x in 85000..100000 {
    //     let k = 10000;
    
        
    //     let prim: String = miller_rabin(x, k);
    //     println!("{} is {}", x, prim);
    // }
}
