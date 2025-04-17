import {render, screen, fireEvent} from "@testing-library/react";
import axios from "axios";
import {vi} from "vitest";
import App from '../src/App';

vi.mock("axios");
const mockedAxios = axios as unknown as vi.Mocked<typeof axios>;

test('renders hello message', () => {
    render(<App/>);
    expect(screen.getByText(/Fetch data/i)).toBeInTheDocument();
});

describe("Fetch data button", () => {
    it("calls the API when the button is clicked", async () => {
        mockedAxios.get.mockResolvedValueOnce({data: {days: ["2025-01-01", "2025-01-02"], variations: [2, -1]}});

        render(<App/>);
        const button = screen.getByText("Fetch data");

        fireEvent.click(button);

        // Wait for DOM update
        const message = await screen.findByText("Points: 2");
        expect(message).toBeInTheDocument();

        // Verify the API was called
        expect(mockedAxios.get).toHaveBeenCalledWith(
            "http://localhost:8000/get_space_objects_variation/",
            {
                "params": {
                    "begin": "2025-01-01",
                    "end": "2025-01-31",
                },
            },
        );
    });
});
