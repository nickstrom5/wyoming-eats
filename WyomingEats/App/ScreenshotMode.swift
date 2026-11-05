import Foundation
import CoreLocation
import UIKit

/// `-screenshot <name>` opens one screen with fixed state for App Store screenshots (scripts/capture-screenshots.sh).
/// Names: home, saloons, steaks, cafes, sweets, farm, pizza, lodges, honors, oldest, detail, map, saved, about.
enum ScreenshotMode {
    /// Debug builds only: an App Store build ignores the launch argument, so no one can reach seeded screens or fake locations.
    static var name: String? {
        #if DEBUG
        let args = ProcessInfo.processInfo.arguments
        guard let i = args.firstIndex(of: "-screenshot"), i + 1 < args.count else { return nil }
        return args[i + 1]
        #else
        return nil
        #endif
    }
    static var isActive: Bool { name != nil }

    @MainActor
    static func apply(to model: AppModel) {
        guard let name, model.isLoaded else { return }
        model.filters = Filters()
        // downtown Casper, the middle of the state, so "nearest" lists have distances without a permission prompt
        model.screenshotLocation = CLLocation(latitude: 42.8501, longitude: -106.3252)
        // by name and town, ignoring case, so a rebuild with a slightly different casing still finds the place; the hand-checked one first
        let pick = { (n: String, town: String?) -> Place? in
            let hits = model.places.filter { $0.name.caseInsensitiveCompare(n) == .orderedSame && (town == nil || $0.city == town) }
            return hits.first(where: \.handChecked) ?? hits.first
        }
        for p in [pick("Million Dollar Cowboy Bar", "Jackson"), pick("Chugwater Soda Fountain", "Chugwater"), pick("Pizza Carrello", "Gillette")]
            .compactMap({ $0 }) where !model.isSaved(p) {
            model.toggleSaved(p)
        }
        let open = { (g: Guide) in model.tab = .guides; model.selectedGuide = g; model.guidesPath = [.guide(g)] }
        switch name {
        case "saloons": open(.saloons)
        case "steaks": open(.steaks)
        case "cafes": open(.cafes)
        case "sweets": open(.sweets)
        case "farm", "pizza":
            // Jackson's Town Square, among its farm-to-table kitchens and pizza
            model.screenshotLocation = CLLocation(latitude: 43.4799, longitude: -110.7624)
            open(name == "farm" ? .farm : .pizza)
        case "lodges": open(.lodges)
        case "honors": open(.honors)
        case "oldest": open(.oldest)
        case "detail":
            // the Million Dollar Cowboy Bar: a historic saloon with its 1937 founding year and its note, seen from the foot of Snow King
            // (half a mile off, so the distance reads as one)
            model.screenshotLocation = CLLocation(latitude: 43.4740, longitude: -110.7560)
            open(.saloons)
            if let p = pick("Million Dollar Cowboy Bar", "Jackson") ?? model.places.first {
                model.selectedPlace = p; model.guidesPath.append(.place(p))
            }
        case "map":
            // Jackson's Town Square: the most picks and honors close together, so the shot shows pins, not one cluster
            model.screenshotLocation = CLLocation(latitude: 43.4799, longitude: -110.7624)
            model.tab = .map
        case "saved": model.tab = .saved
        case "about": model.tab = .about
        default: model.tab = .guides; model.selectedGuide = nil
        }
        // iPad shows the place column next to every list, so give each shot a place instead of "Pick a place": a different
        // honored or hand-checked one per shot.
        guard UIDevice.current.userInterfaceIdiom == .pad, model.selectedPlace == nil else { return }
        let place: Place? = switch name {
        case "home": pick("Million Dollar Cowboy Bar", "Jackson")
        case "saloons": pick("Mint Bar", "Sheridan")
        case "steaks": pick("Gun Barrel Steak and Game House", "Jackson")
        case "cafes": pick("Cowboy Cafe", "Dubois")
        case "sweets": pick("Chugwater Soda Fountain", "Chugwater")
        case "farm": pick("Gather", "Jackson")
        case "pizza": pick("Pizza Carrello", "Gillette")
        case "lodges": pick("Irma Restaurant Grill", "Cody")
        case "map": pick("Million Dollar Cowboy Bar", "Jackson")
        case "honors": pick("Nora's Fish Creek Inn", "Wilson")
        case "oldest": pick("Miners and Stockmen's", "Hartville")
        case "saved": pick("Chugwater Soda Fountain", "Chugwater")
        case "about": nil
        default: pick("Million Dollar Cowboy Bar", "Jackson")
        }
        model.selectedPlace = place
    }
}
