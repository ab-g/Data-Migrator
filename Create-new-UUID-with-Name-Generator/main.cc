#include <iostream>
#include <stduuid/uuid.h>

using namespace uuids;

int main(int argc, char* argv[])
{
    uuid const empty;
    uuids::uuid_name_generator gen(empty);
    if (argc > 1)
        std::cout << uuids::to_string(gen(argv[1]));
    return 0;
}
