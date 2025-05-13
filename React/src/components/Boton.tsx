
interface Propiedades {
    Children: string;
    onClick?: () => void;
}

const Boton = ({Children, onClick}: Propiedades) => {
    return (
        <>
            <button type="button" className="btn btn-primary" onClick={onClick}>{Children}</button>
        </>
    );
}

export default Boton;
