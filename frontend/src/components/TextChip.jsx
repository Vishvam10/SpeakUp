function TextChip({ category, message, color, big = false }) {
  console.log("Big prop:", big);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "flexStart",
        textAlign: "left",
        width: "10rem",
        height: "auto",
        padding: "1.2rem",
        margin: "1rem",
        border: `1px solid ${color}`,
        borderRadius: "1rem",
        backgroundColor: "#242424",
        color: "white",
      }}
    >
      <h5
        style={{
          fontSize: "0.8rem",
          fontWeight: "bold",
          margin: "0rem 0rem -1rem 0rem",
        }}
      >
        {category}
      </h5>
      

      <p
        style={{
        fontSize: big === true ? "4.2rem" : "0.8rem",
          fontWeight: big === true ? "bold" : "normal",
          margin: "1rem 0rem 0rem 0rem",
        }}
      >
        {message}
      </p>
    </div>
  );
}

export default TextChip;
