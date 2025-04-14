library ieee;
use ieee.std_logic_1164.all;
use work.all;

entity test_module is
generic(
    param1 : integer := 10;
    param2 : integer := 20
);
port(
    input1: in std_logic;
    output1: out std_logic
);
end entity test_module;
architecture Behavioral of test_module is 
    constant const1 : integer := 42;
    signal signal1 : std_logic_vector(7 downto 0);

begin
    output1 <= input1;
    init : entity work.test
    generic map(
        p => param1
    )
    port map(
        a => "0",
        b => input1
    );

end architecture Behavioral;
