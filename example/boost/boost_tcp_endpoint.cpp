#include <boost/asio.hpp>
#include <iostream>

using namespace boost;

int main()
{
    std::string raw_ip_address = "127.0.0.1";
    unsigned short port_num = 1234;

    // Create the endpoint
    asio::ip::tcp::endpoint ep(asio::ip::address::from_string(raw_ip_address), port_num);
    std::cout << "ep = " << ep << "\n";

    asio::io_service ios;

    // Create a socket
    asio::ip::tcp::socket sock(ios, ep.protocol());

    std::cout << "local0: " << sock.local_endpoint()  << "\n";

    // Connecting the socket.
    sock.connect(ep);

    std::cout << "local:  " << sock.local_endpoint()  << "\n";
    std::cout << "remote: " << sock.remote_endpoint()  << "\n";

    return 0;
}
