from collections import deque
import argparse


class Airport:
    def __init__(self, code):
        self.code = code

    def __eq__(self, other):
        return hasattr(other, 'code') and self.code == other.code

    def __hash__(self):
        return hash(self.code)

    def __repr__(self):
        return self.code


class Route:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


class AirlineRoutes:

    def __init__(self):
        self.routes = dict()

    def addRoute(self, route):
        if route.source in self.routes.keys():
            self.routes[route.source].append(route.destination)
        else:
            self.routes[route.source] = [route.destination]

    def findRoute(self, departure, destination, stops=3):
        result = set()
        q = deque()
        q.append([departure])
        while len(q) != 0:
            path = q.popleft()
            last_stop = path[-1]

            # Destination is found
            if last_stop == destination:
                hashable_path = tuple(path)
                if hashable_path not in result:
                    result.add(hashable_path)
                    print(str(calc_stops(path)) + ":" + str(hashable_path))

            # Continue to search paths
            if last_stop in self.routes:
                destinations = self.routes[last_stop]
                for dest in destinations:
                    if dest not in path:
                        new_path = path + [dest]
                        current_stops = calc_stops(new_path)
                        if current_stops <= stops:
                            q.append(new_path)
        return result


def calc_stops(path):
    return len(path) - 2


def parse_routes(routes_dir):
    airline_routes = AirlineRoutes()
    routes = open(routes_dir)
    for route in routes:
        route_parts = route.split(',')
        source = Airport(route_parts[2])
        destination = Airport(route_parts[4])
        airline_routes.addRoute(Route(source, destination))
    return airline_routes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input path to the airlines DB')
    parser.add_argument('airlinesDb', metavar='-ADB', help='Absolute path to the airlines DB')
    parser.add_argument('source', metavar='-SRC', help='Source airport')
    parser.add_argument('destination', metavar='-DST', help='Destination airport')
    parser.add_argument('stops', metavar='-S', type=int, default=3, help='Max stops')
    args = parser.parse_args()

    airlines_routes = parse_routes(args.airlinesDb)
    route = airlines_routes.findRoute(Airport(args.source), Airport(args.destination), args.stops)

    print(route)
