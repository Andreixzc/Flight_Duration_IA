import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

public class Parser2 {
    public static void main(String[] args) {
        String sortedPositionsCsv = "E:/Projetos/TesteTecnico/Dataset/PosSorted/11.csv";
        parse(sortedPositionsCsv);
    }

    public static void parse(String filename) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");
        ArrayList<Position> positions = new ArrayList<>();
        ArrayList<Flight> voos = new ArrayList<>();
        
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filename));
            String line = reader.readLine(); // Ler e descartar o cabeçalho
            
            while ((line = reader.readLine()) != null) {
                String[] fields = line.split(",");
                Position currentPosition = new Position();
                currentPosition.time = fields[0];
                currentPosition.latitude = Double.parseDouble(fields[1]);
                currentPosition.longitude = Double.parseDouble(fields[2]);
                currentPosition.altitude = Double.parseDouble(fields[3]);
                currentPosition.groundSpeed = Double.parseDouble(fields[4]);
                currentPosition.idAircraft = fields[5];
                currentPosition.modelAircraft = fields[6];
                positions.add(currentPosition);
            }
            
            reader.close();
            
            // Processar as posições para segmentar voos
            for (int i = 0; i < positions.size(); i++) {
                Position start = positions.get(i);
                Position end = start;
                for (int j = i + 1; j < positions.size(); j++) {
                    Position next = positions.get(j);
                    if (isIntervalGreaterThanThreeMinutes(sdf, end.time, next.time)) {
                        break;
                    } else {
                        end = next;
                    }
                }
                if (end != start) {
                    Flight flight = new Flight();
                    flight.saida = start.time;
                    flight.chegada = end.time;
                    voos.add(flight);
                    // Avançar o ponteiro de análise
                    i = positions.indexOf(end);
                }
            }
            
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        System.out.println("Voos segmentados:");
        for (Flight voo : voos) {
            System.out.println(voo);
        }
    }

    public static boolean isIntervalGreaterThanThreeMinutes(SimpleDateFormat sdf, String date1, String date2) {
        try {
            Date d1 = sdf.parse(date1);
            Date d2 = sdf.parse(date2);
            long diffInMillies = Math.abs(d2.getTime() - d1.getTime());
            long diffInMinutes = diffInMillies / (1000 * 60);
            return diffInMinutes > 5;
        } catch (Exception e) {
            System.out.println("Erro ao comparar datas: " + e.getMessage());
            return false;
        }
    }
}

class Position {
    String time;
    double latitude;
    double longitude;
    double altitude;
    double groundSpeed;
    String idAircraft;
    String modelAircraft;

    @Override
    public String toString() {
        return "Position{" +
                "time='" + time + '\'' +
                ", latitude=" + latitude +
                ", longitude=" + longitude +
                ", altitude=" + altitude +
                ", groundSpeed=" + groundSpeed +
                ", idAircraft='" + idAircraft + '\'' +
                ", modelAircraft='" + modelAircraft + '\'' +
                '}';
    }
}

class Flight {
    public String saida;
    public String chegada;

    @Override
    public String toString() {
        return "Flight [saida=" + saida + ", chegada=" + chegada + "]";
    }
}
