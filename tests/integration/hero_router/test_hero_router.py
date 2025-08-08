import pytest
from fastapi import status
from httpx import AsyncClient

# ===== POST /hero/ Tests =====


@pytest.mark.parametrize(
    "name,expected_status",
    [
        pytest.param("batman", status.HTTP_204_NO_CONTENT, id="known_hero_batman"),
        pytest.param("Superman", status.HTTP_204_NO_CONTENT, id="known_hero_superman"),
        pytest.param("Iron Man", status.HTTP_204_NO_CONTENT, id="known_hero_iron_man"),
        pytest.param("invalid", status.HTTP_404_NOT_FOUND, id="unknown_hero"),
        pytest.param(
            "nonexistent_hero_xyz", status.HTTP_404_NOT_FOUND, id="nonexistent_hero"
        ),
    ],
)
async def test_enlisting_hero(
    app_client: AsyncClient,
    name: str,
    expected_status: int,
):
    """Test enlisting a hero by name."""

    response = await app_client.post(f"/hero/?name={name}")
    assert response.status_code == expected_status


async def test_enlisting_hero_case_insensitive(app_client: AsyncClient):
    """Test that hero search is case insensitive."""

    test_cases = ["batman", "Batman", "BATMAN", "BaTmAn"]

    for name in test_cases:
        response = await app_client.post(f"/hero/?name={name}")
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f"Failed for name: {name}"
        )


async def test_enlisting_hero_already_exists(app_client: AsyncClient):
    """Test enlisting the same hero multiple times."""

    # First enlistment
    response1 = await app_client.post("/hero/?name=batman")
    assert response1.status_code == status.HTTP_204_NO_CONTENT

    # Second enlistment of same hero should still succeed (overwrite)
    response2 = await app_client.post("/hero/?name=batman")
    assert response2.status_code == status.HTTP_204_NO_CONTENT


async def test_enlisting_hero_missing_name_parameter(app_client: AsyncClient):
    """Test POST /hero/ without name parameter."""

    response = await app_client.post("/hero/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_enlisting_hero_empty_name(app_client: AsyncClient):
    """Test POST /hero/ with empty name."""

    response = await app_client.post("/hero/?name=")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_enlisting_hero_multiple_heroes_found(app_client: AsyncClient):
    """Test POST /hero/ when API returns multiple heroes but none match exactly."""

    response = await app_client.post("/hero/?name=bat")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_enlisting_hero_whitespace_handling(app_client: AsyncClient):
    """Test POST /hero/ with names containing whitespace."""

    response = await app_client.post("/hero/?name=batman")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await app_client.post("/hero/?name= batman ")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_enlisting_hero_special_characters(app_client: AsyncClient):
    """Test POST /hero/ with special characters in name."""

    response = await app_client.post("/hero/?name=Iron Man")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await app_client.post("/hero/?name=Iron%20Man")
    assert response.status_code == status.HTTP_204_NO_CONTENT


# ===== GET /hero/ Tests =====


async def test_get_heroes_no_filters(app_client: AsyncClient):
    """Test getting all heroes without any filters."""

    # First, enlist some heroes
    await app_client.post("/hero/?name=batman")
    await app_client.post("/hero/?name=Superman")
    await app_client.post("/hero/?name=Iron Man")

    response = await app_client.get("/hero/")
    assert response.status_code == status.HTTP_200_OK

    heroes = response.json()
    assert isinstance(heroes, list)
    assert len(heroes) >= 3

    # Check that all enlisted heroes are present
    hero_names = [hero["name"] for hero in heroes]
    assert "Batman" in hero_names
    assert "Superman" in hero_names
    assert "Iron Man" in hero_names


async def test_get_heroes_by_exact_name(app_client: AsyncClient):
    """Test filtering heroes by exact name."""

    # Enlist heroes
    await app_client.post("/hero/?name=batman")
    await app_client.post("/hero/?name=Superman")

    # Test exact name match for Batman
    response = await app_client.get("/hero/?name=Batman")
    assert response.status_code == status.HTTP_200_OK

    heroes = response.json()
    assert len(heroes) == 1
    assert heroes[0]["name"] == "Batman"


async def test_get_heroes_by_name_case_insensitive(app_client: AsyncClient):
    """Test that name filtering is case insensitive."""

    await app_client.post("/hero/?name=batman")

    test_cases = ["batman", "Batman", "BATMAN", "BaTmAn"]

    for name in test_cases:
        response = await app_client.get(f"/hero/?name={name}")
        assert response.status_code == status.HTTP_200_OK
        heroes = response.json()
        assert len(heroes) == 1
        assert heroes[0]["name"] == "Batman"


async def test_get_heroes_intelligence_filters(app_client: AsyncClient):
    """Test filtering heroes by intelligence ranges."""

    # Enlist heroes with different intelligence levels
    # Batman: Intelligence=81, Superman: Intelligence=94, Iron Man: Intelligence=100, A-Bomb: Intelligence=38
    await app_client.post("/hero/?name=batman")
    await app_client.post("/hero/?name=Superman")
    await app_client.post("/hero/?name=Iron Man")
    await app_client.post("/hero/?name=A-Bomb")

    # Test intelligenceFrom (>=)
    response = await app_client.get("/hero/?intelligenceFrom=90")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Superman" in hero_names  # 94
    assert "Iron Man" in hero_names  # 100
    assert "Batman" not in hero_names  # 81
    assert "A-Bomb" not in hero_names  # 38

    # Test intelligenceTo (<=)
    response = await app_client.get("/hero/?intelligenceTo=50")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "A-Bomb" in hero_names  # 38
    assert "Batman" not in hero_names  # 81

    # Test range filtering
    response = await app_client.get("/hero/?intelligenceFrom=80&intelligenceTo=95")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Batman" in hero_names  # 81
    assert "Superman" in hero_names  # 94
    assert "Iron Man" not in hero_names  # 100


async def test_get_heroes_strength_filters(app_client: AsyncClient):
    """Test filtering heroes by strength ranges."""

    # Batman: Strength=40, Superman: Strength=100, A-Bomb: Strength=100, Iron Man: Strength=85
    await app_client.post("/hero/?name=batman")
    await app_client.post("/hero/?name=Superman")
    await app_client.post("/hero/?name=A-Bomb")
    await app_client.post("/hero/?name=Iron Man")

    # Test strengthFrom (>=)
    response = await app_client.get("/hero/?strengthFrom=90")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Superman" in hero_names  # 100
    assert "A-Bomb" in hero_names  # 100
    assert "Iron Man" not in hero_names  # 85
    assert "Batman" not in hero_names  # 40

    # Test strengthTo (<=)
    response = await app_client.get("/hero/?strengthTo=50")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Batman" in hero_names  # 40


async def test_get_heroes_speed_filters(app_client: AsyncClient):
    """Test filtering heroes by speed ranges."""

    # Batman: Speed=29, Superman: Speed=100, Iron Man: Speed=58, A-Bomb: Speed=17
    await app_client.post("/hero/?name=batman")
    await app_client.post("/hero/?name=Superman")
    await app_client.post("/hero/?name=Iron Man")
    await app_client.post("/hero/?name=A-Bomb")

    # Test speedFrom (>=)
    response = await app_client.get("/hero/?speedFrom=50")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Superman" in hero_names  # 100
    assert "Iron Man" in hero_names  # 58
    assert "Batman" not in hero_names  # 29

    # Test speedTo (<=)
    response = await app_client.get("/hero/?speedTo=30")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Batman" in hero_names  # 29
    assert "A-Bomb" in hero_names  # 17


async def test_get_heroes_power_filters(app_client: AsyncClient):
    """Test filtering heroes by power ranges."""

    # Batman: Power=63, Superman: Power=100, Iron Man: Power=100, A-Bomb: Power=24
    await app_client.post("/hero/?name=batman")
    await app_client.post("/hero/?name=Superman")
    await app_client.post("/hero/?name=Iron Man")
    await app_client.post("/hero/?name=A-Bomb")

    # Test powerFrom (>=)
    response = await app_client.get("/hero/?powerFrom=90")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Superman" in hero_names  # 100
    assert "Iron Man" in hero_names  # 100
    assert "Batman" not in hero_names  # 63

    # Test powerTo (<=)
    response = await app_client.get("/hero/?powerTo=50")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "A-Bomb" in hero_names  # 24


async def test_get_heroes_combined_filters(app_client: AsyncClient):
    """Test filtering heroes with multiple criteria."""

    await app_client.post("/hero/?name=batman")
    await app_client.post("/hero/?name=Superman")
    await app_client.post("/hero/?name=Iron Man")
    await app_client.post("/hero/?name=A-Bomb")

    # Test combined filters: high intelligence AND high strength
    response = await app_client.get("/hero/?intelligenceFrom=90&strengthFrom=90")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Superman" in hero_names  # Int=94, Str=100
    assert "Iron Man" not in hero_names  # Int=100, Str=85 (strength too low)

    # Test name filter combined with stats
    response = await app_client.get("/hero/?name=Batman&intelligenceFrom=80")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    assert len(heroes) == 1
    assert heroes[0]["name"] == "Batman"

    # Test name filter that should exclude the hero due to stats
    response = await app_client.get("/hero/?name=Batman&strengthFrom=100")
    # Batman has strength=40, not >=100
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_heroes_with_null_stats(app_client: AsyncClient):
    """Test filtering heroes that have null stats."""

    # Agent 13 has: Intelligence=null, Strength=46, Speed=null, Power=null
    await app_client.post("/hero/?name=Agent 13")
    await app_client.post("/hero/?name=batman")

    # First verify both heroes are in database
    response = await app_client.get("/hero/")
    assert response.status_code == status.HTTP_200_OK
    all_heroes = response.json()
    all_names = [hero["name"] for hero in all_heroes]
    assert "Batman" in all_names
    assert "Agent 13" in all_names

    # Heroes with null intelligence should not match intelligence filters
    response = await app_client.get("/hero/?intelligenceFrom=1")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Batman" in hero_names
    assert "Agent 13" not in hero_names  # null intelligence doesn't match >=1

    # But they should match strength filters if strength is not null
    response = await app_client.get("/hero/?strengthFrom=40")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Agent 13" in hero_names  # strength=46 >= 40
    assert "Batman" in hero_names  # strength=40 >= 40


async def test_get_heroes_no_matches(app_client: AsyncClient):
    """Test GET /hero/ when no heroes match the filters."""

    await app_client.post("/hero/?name=batman")

    # Filter that should match no heroes
    response = await app_client.get("/hero/?strengthFrom=999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_heroes_nonexistent_name(app_client: AsyncClient):
    """Test GET /hero/ with a name that doesn't exist in database."""

    await app_client.post("/hero/?name=batman")

    response = await app_client.get("/hero/?name=NonexistentHero")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_heroes_empty_database(app_client: AsyncClient):
    """Test GET /hero/ when no heroes are enlisted."""

    response = await app_client.get("/hero/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_heroes_invalid_parameter_values(app_client: AsyncClient):
    """Test GET /hero/ with invalid parameter values."""

    await app_client.post("/hero/?name=batman")
    await app_client.post("/hero/?name=superman")

    # Test negative values (should be handled gracefully)
    response = await app_client.get("/hero/?intelligenceFrom=-10")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Batman" in hero_names
    assert "Superman" in hero_names

    # Test very large values
    response = await app_client.get("/hero/?strengthTo=999999")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    hero_names = [hero["name"] for hero in heroes]
    assert "Batman" in hero_names
    assert "Superman" in hero_names


async def test_get_heroes_malformed_query_parameters(app_client: AsyncClient):
    """Test GET /hero/ with malformed query parameters."""

    response = await app_client.get("/hero/?intelligenceFrom=not_a_number")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = await app_client.get("/hero/?strengthFrom=abc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_heroes_boundary_values(app_client: AsyncClient):
    """Test GET /hero/ with boundary values."""

    await app_client.post("/hero/?name=batman")  # Intelligence=81

    # Test exact boundary matches
    response = await app_client.get("/hero/?intelligenceFrom=81")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    assert len(heroes) == 1

    response = await app_client.get("/hero/?intelligenceTo=81")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    assert len(heroes) == 1

    # Test just outside boundaries
    response = await app_client.get("/hero/?intelligenceFrom=82")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = await app_client.get("/hero/?intelligenceTo=80")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_heroes_zero_values(app_client: AsyncClient):
    """Test GET /hero/ with zero values in filters."""

    await app_client.post("/hero/?name=batman")

    # Test zero values (should work normally)
    response = await app_client.get("/hero/?intelligenceFrom=0")
    assert response.status_code == status.HTTP_200_OK
    heroes = response.json()
    assert len(heroes) == 1

    response = await app_client.get("/hero/?strengthTo=0")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_database_isolation_between_tests(app_client: AsyncClient):
    """Test that database state doesn't leak between tests."""

    # Database should start empty due to our clear_hero_database fixture
    response = await app_client.get("/hero/")
    assert response.status_code == status.HTTP_404_NOT_FOUND, (
        "Database should be empty at start of test"
    )

    # Add a hero
    await app_client.post("/hero/?name=batman")

    # Verify hero was added
    response = await app_client.get("/hero/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


async def test_get_heroes_response_structure(app_client: AsyncClient):
    """Test that GET /hero/ returns correctly structured hero data."""

    await app_client.post("/hero/?name=batman")

    response = await app_client.get("/hero/?name=Batman")
    assert response.status_code == status.HTTP_200_OK

    heroes = response.json()
    assert isinstance(heroes, list)
    assert len(heroes) == 1

    hero = heroes[0]

    # Verify hero structure matches the Hero model
    assert "id" in hero
    assert "name" in hero
    assert "powerstats" in hero

    assert isinstance(hero["id"], int)
    assert isinstance(hero["name"], str)
    assert isinstance(hero["powerstats"], dict)

    # Verify powerstats structure
    powerstats = hero["powerstats"]
    expected_stats = ["intelligence", "strength", "speed", "power"]

    for stat in expected_stats:
        assert stat in powerstats
        # Stats can be int or None
        assert powerstats[stat] is None or isinstance(powerstats[stat], int)

    # Verify specific hero data
    assert hero["name"] == "Batman"
    assert hero["id"] == 69  # Based on our earlier inspection
    assert hero["powerstats"]["intelligence"] == 81
    assert hero["powerstats"]["strength"] == 40


# ===== Integration Tests =====


async def test_full_workflow(app_client: AsyncClient):
    """Test complete workflow: enlist multiple heroes and filter them."""

    # Enlist several heroes
    heroes_to_enlist = ["batman", "Superman", "Iron Man", "A-Bomb", "Agent 13"]

    for hero_name in heroes_to_enlist:
        response = await app_client.post(f"/hero/?name={hero_name}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify all heroes are in database
    response = await app_client.get("/hero/")
    assert response.status_code == status.HTTP_200_OK
    all_heroes = response.json()
    assert len(all_heroes) == len(heroes_to_enlist)

    # Test various filters
    # High intelligence heroes
    response = await app_client.get("/hero/?intelligenceFrom=90")
    assert response.status_code == status.HTTP_200_OK
    smart_heroes = response.json()
    smart_names = [h["name"] for h in smart_heroes]
    assert "Superman" in smart_names
    assert "Iron Man" in smart_names

    # Strong heroes
    response = await app_client.get("/hero/?strengthFrom=85")
    assert response.status_code == status.HTTP_200_OK
    strong_heroes = response.json()
    strong_names = [h["name"] for h in strong_heroes]
    assert "Superman" in strong_names
    assert "A-Bomb" in strong_names

    # Specific hero by name
    response = await app_client.get("/hero/?name=Batman")
    assert response.status_code == status.HTTP_200_OK
    batman_result = response.json()
    assert len(batman_result) == 1
    assert batman_result[0]["name"] == "Batman"
