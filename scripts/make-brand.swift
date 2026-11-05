// Cowboy State Eats brand (provisional, 2026-11-05; Nick picks the name, icon and palette): the app icon is concept C of
// scripts/icon-concepts.swift, a root beer float from the soda fountain, on sagebrush; the shared Eats Ranked icon style,
// state-prompts/ICON-STYLE.md, no backing shape. No bucking horse and rider (the state's registered trademark), no University of Wyoming
// brown and gold, no seal or flag.
// Usage, from wy-eats/: swift scripts/make-brand.swift   -> WyomingEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png,
// docs/ favicons and touch icons, docs/og.png. scripts/make-site.py draws the same mark as its inline SVG: change both together.
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let SAGE: UInt32 = 0x3E4F3A, GLASS: UInt32 = 0xDCE6E8, SODA: UInt32 = 0x6B3A1F, CREAM: UInt32 = 0xF4EBDD, CHERRY: UInt32 = 0xB0172B
let STRAW: UInt32 = 0xC23B2E, TETON: UInt32 = 0x2B5C8A, RUST: UInt32 = 0x8C3B2A, SAGE2: UInt32 = 0x56694F, WHEAT: UInt32 = 0xD9A441
let PAGE: UInt32 = 0xF6F1E7

/// C: the root beer float. CoreGraphics y-up, s = canvas size. Identical to icon-concepts.swift's concept C.
func float(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(STRAW))   // the straw first, behind the scoop
    c.saveGState(); c.translateBy(x: 0.58 * s, y: 0.66 * s); c.rotate(by: -0.45)
    c.fill(CGRect(x: 0, y: 0, width: 0.035 * s, height: 0.21 * s)); c.restoreGState()
    let glass = CGMutablePath()   // a flared fountain glass
    glass.move(to: CGPoint(x: 0.41 * s, y: 0.15 * s)); glass.addLine(to: CGPoint(x: 0.59 * s, y: 0.15 * s))
    glass.addLine(to: CGPoint(x: 0.67 * s, y: 0.68 * s)); glass.addLine(to: CGPoint(x: 0.33 * s, y: 0.68 * s)); glass.closeSubpath()
    c.setFillColor(rgb(GLASS)); c.addPath(glass); c.fillPath()
    let soda = CGMutablePath()
    soda.move(to: CGPoint(x: 0.425 * s, y: 0.18 * s)); soda.addLine(to: CGPoint(x: 0.575 * s, y: 0.18 * s))
    soda.addLine(to: CGPoint(x: 0.635 * s, y: 0.62 * s)); soda.addLine(to: CGPoint(x: 0.365 * s, y: 0.62 * s)); soda.closeSubpath()
    c.setFillColor(rgb(SODA)); c.addPath(soda); c.fillPath()
    c.setFillColor(rgb(CREAM)); c.fillEllipse(in: CGRect(x: 0.31 * s, y: 0.60 * s, width: 0.38 * s, height: 0.17 * s))
    c.setFillColor(rgb(CHERRY)); c.fillEllipse(in: CGRect(x: 0.46 * s, y: 0.75 * s, width: 0.08 * s, height: 0.08 * s))
}

func render(_ n: Int, _ path: String, background: Bool) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: background ? CGImageAlphaInfo.noneSkipLast.rawValue : CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.setShouldAntialias(true)
    if background { ctx.setFillColor(rgb(SAGE)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n)) }
    float(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
render(1024, "WyomingEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png", background: true)
try? FileManager.default.createDirectory(atPath: "docs", withIntermediateDirectories: true)
for (n, name) in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")] {
    render(n, "docs/" + name, background: true)
}

/// The share image (1200 x 630): sagebrush, the float at the left, the name and tagline at the right, and the app's header band along
/// the bottom: the Tetons in Teton blue, red-rock foothills and the plains, over a prairie-wheat baseline, on cream (Theme.swift's
/// Stripes.ridges).
func og(_ path: String) {
    let W = 1200, H = 630
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(SAGE)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    let band: CGFloat = 70, base: CGFloat = 14
    ctx.setFillColor(rgb(PAGE)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: Int(band)))
    let ridges: [[(CGFloat, CGFloat)]] = [
        [(0, 0.55), (0.08, 0.62), (0.16, 0.58), (0.24, 0.80), (0.29, 1.0), (0.33, 0.78), (0.37, 0.92), (0.42, 0.70), (0.52, 0.62),
         (0.64, 0.66), (0.76, 0.58), (0.88, 0.64), (1, 0.60)],
        [(0, 0.36), (0.12, 0.44), (0.26, 0.38), (0.44, 0.50), (0.60, 0.40), (0.74, 0.48), (0.90, 0.38), (1, 0.42)],
        [(0, 0.16), (0.20, 0.20), (0.40, 0.15), (0.60, 0.19), (0.80, 0.14), (1, 0.18)]]
    let fills = [rgb(TETON).copy(alpha: 0.7)!, rgb(RUST), rgb(SAGE2)]
    for (i, ridge) in ridges.enumerated() {
        let p = CGMutablePath(); p.move(to: CGPoint(x: 0, y: base))
        for (x, rise) in ridge { p.addLine(to: CGPoint(x: x * CGFloat(W), y: base + (band - base) * rise)) }
        p.addLine(to: CGPoint(x: CGFloat(W), y: base)); p.closeSubpath()
        ctx.setFillColor(fills[i]); ctx.addPath(p); ctx.fillPath()
    }
    ctx.setFillColor(rgb(WHEAT)); ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(W), height: base))
    ctx.saveGState(); ctx.translateBy(x: 30, y: 90); float(ctx, 500); ctx.restoreGState()
    let ns = NSGraphicsContext(cgContext: ctx, flipped: false)
    NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ns
    let title = NSFont(name: "AvenirNextCondensed-Heavy", size: 80) ?? NSFont.boldSystemFont(ofSize: 70)
    let sub = NSFont(name: "AvenirNextCondensed-DemiBold", size: 34) ?? NSFont.boldSystemFont(ofSize: 30)
    NSAttributedString(string: "COWBOY STATE", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 560, y: 380))
    NSAttributedString(string: "EATS", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 560, y: 296))
    NSAttributedString(string: "SALOONS, STEAKS & SODA FOUNTAINS", attributes: [.font: sub, .foregroundColor: NSColor(srgbRed: 0.851, green: 0.643, blue: 0.255, alpha: 1)]).draw(at: NSPoint(x: 564, y: 246))
    NSGraphicsContext.restoreGraphicsState()
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
og("docs/og.png")
