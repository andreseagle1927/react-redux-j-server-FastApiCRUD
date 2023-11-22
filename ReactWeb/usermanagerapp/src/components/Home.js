import React, { useState, useEffect } from 'react';
import { Carousel, Container, Card, ProgressBar, Button } from 'react-bootstrap';

const baseUrl = "https://localhost:5001/api/Libros";

export function Home() {
  const [data, setData] = useState([]);
  const [currentLibro, setCurrentLibro] = useState({
    id: '',
    titulo: '',
    autor: '',
    precio: 0,
    cantidad: 0,
    imagen: ''
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(baseUrl);
        const librosData = await response.json();
        setData(librosData);
        if (librosData.length > 0) {
          setCurrentLibro(librosData[0]);
        }
      } catch (error) {
        console.error('Error al cargar datos:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <Container>
      <h1 className="text-center" style={{ color: 'white' }}>Libros Carousel</h1>

      <Carousel
        interval={null} // Desactiva la transición automática
        nextLabel=""
        prevLabel=""
        indicators={false}
        controls={data.length > 3}
      >
        {data.map((libro, index) => (
          <Carousel.Item key={index}>
            <div className="d-flex justify-content-around">
              {data.slice(index, index + 3).map((libro, subIndex) => (
                <Card key={subIndex} className="yugioh-card">
                  <Card.Img variant="top" src={libro.imagen} alt={libro.titulo} />
                  <Card.Body>
                    <Card.Title>{libro.titulo}</Card.Title>
                    <Card.Text>Autor: {libro.autor}</Card.Text>
                    <Card.Text>Precio: {libro.precio}</Card.Text>
                    <Card.Text>Cantidad: {libro.cantidad}</Card.Text>
                    <ProgressBar now={libro.precio} max={100} label={`Precio: ${libro.precio}`} />
                    <Button variant="primary" onClick={() => setCurrentLibro(libro)}>Detalles</Button>
                  </Card.Body>
                </Card>
              ))}
            </div>
          </Carousel.Item>
        ))}
      </Carousel>
    </Container>
  );
}
